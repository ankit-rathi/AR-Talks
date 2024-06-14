# Import required libraries
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.python_sensor import PythonSensor
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from kafka import KafkaConsumer
from datetime import datetime, timedelta
import boto3
import psycopg2

# Kafka configuration
KAFKA_TOPIC = 'your_kafka_topic'
KAFKA_BOOTSTRAP_SERVERS = 'your_kafka_bootstrap_servers'

# AWS configuration
AWS_REGION = 'your_aws_region'
RDS_HOST = 'your_rds_host'
RDS_PORT = 'your_rds_port'
RDS_DB = 'your_rds_db'
RDS_USER = 'your_rds_user'
RDS_PASSWORD = 'your_rds_password'

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'kafka_to_emr_to_rds',
    default_args=default_args,
    description='Poll Kafka topic, process message with EMR, and write to RDS',
    schedule_interval=timedelta(days=1),
)

# Function to poll Kafka topic for incoming messages
def poll_kafka_topic():
    # Create a Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group'
    )

    # Poll for messages
    for message in consumer:
        # Assuming a single message is processed for simplicity
        return message.value.decode('utf-8')

# Function to create an EMR Serverless connection if a message arrives
def create_emr_serverless_connection(ti):
    # Fetch message from the previous task
    message = ti.xcom_pull(task_ids='poll_kafka_topic')
    
    # Initialize EMR Serverless client
    emr_client = boto3.client('emr-serverless', region_name=AWS_REGION)
    
    # Define EMR serverless application details and create the application
    response = emr_client.create_application(
        name='emr-serverless-app',
        releaseLabel='emr-6.4.0',
        type='HIVE'
    )
    app_id = response['applicationId']
    
    # Store the application ID for further use
    ti.xcom_push(key='app_id', value=app_id)

    return app_id

# Function to write the message to AWS RDS (Postgres) via EMR
def write_to_rds_via_emr(ti):
    # Fetch the message and application ID from previous tasks
    message = ti.xcom_pull(task_ids='poll_kafka_topic')
    app_id = ti.xcom_pull(task_ids='create_emr_serverless_connection', key='app_id')

    # Connect to AWS RDS (Postgres)
    conn = psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        database=RDS_DB,
        user=RDS_USER,
        password=RDS_PASSWORD
    )
    cursor = conn.cursor()
    
    # Insert the message into the RDS table
    cursor.execute("INSERT INTO your_table (message) VALUES (%s)", (message,))
    conn.commit()
    
    # Close the database connection
    cursor.close()
    conn.close()

# Task to poll the Kafka topic for incoming messages
poll_kafka_task = PythonSensor(
    task_id='poll_kafka_topic',
    python_callable=poll_kafka_topic,
    mode='poke',  # Use 'poke' mode to keep checking until a message is received
    timeout=600,  # Timeout after 10 minutes if no message is received
    poke_interval=10,  # Check every 10 seconds
    dag=dag,
)

# Task to create an EMR Serverless connection if a message arrives
create_emr_task = PythonOperator(
    task_id='create_emr_serverless_connection',
    python_callable=create_emr_serverless_connection,
    provide_context=True,  # Provide context to access XCom values
    dag=dag,
)

# Task to write the message to AWS RDS (Postgres) via EMR
write_to_rds_task = PythonOperator(
    task_id='write_to_rds_via_emr',
    python_callable=write_to_rds_via_emr,
    provide_context=True,  # Provide context to access XCom values
    dag=dag,
)

# Define the task dependencies
poll_kafka_task >> create_emr_task >> write_to_rds_task
