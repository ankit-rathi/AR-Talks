from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator, EmrStepSensor
from airflow.utils.dates import days_ago
import boto3
import json
from kafka import KafkaConsumer

# Function to retrieve secrets from AWS Secrets Manager
def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-west-2'  # Replace with your region
    )
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

# Task function to check for new messages in Kafka
def check_for_kafka_messages(**kwargs):
    # Retrieve secrets
    kafka_secrets = get_secret('kafka_secrets')
    
    # Kafka Consumer configuration
    consumer = KafkaConsumer(
        'your_kafka_topic',  # Replace with your Kafka topic
        bootstrap_servers=kafka_secrets['bootstrap_servers'],
        security_protocol='SSL',
        ssl_cafile=kafka_secrets['ssl_cafile'],
        ssl_certfile=kafka_secrets['ssl_certfile'],
        ssl_keyfile=kafka_secrets['ssl_keyfile'],
        group_id='your_consumer_group',  # Replace with your consumer group
        auto_offset_reset='earliest'
    )
    
    # Check for new messages
    messages = consumer.poll(timeout_ms=5000)
    consumer.close()
    
    # If there are new messages, push True to XCom
    if messages:
        kwargs['ti'].xcom_push(key='new_messages', value=True)
    else:
        kwargs['ti'].xcom_push(key='new_messages', value=False)

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG(
    'kafka_to_rds',
    default_args=default_args,
    description='Consume Kafka messages and store in RDS using EMR',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False
)

# Task to check for new Kafka messages
check_kafka_task = PythonOperator(
    task_id='check_kafka_messages',
    provide_context=True,
    python_callable=check_for_kafka_messages,
    dag=dag
)

# EMR Steps
emr_steps = [
    {
        'Name': 'Store Kafka Messages in RDS',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                's3://your-bucket/path/to/your_script.py'  # Replace with your script path
            ]
        }
    }
]

# Task to add steps to EMR cluster
add_emr_steps = EmrAddStepsOperator(
    task_id='add_emr_steps',
    job_flow_id='your_emr_cluster_id',  # Replace with your EMR cluster ID
    steps=emr_steps,
    aws_conn_id='aws_default',
    dag=dag
)

# Task to wait for the EMR step to complete
wait_for_emr_step = EmrStepSensor(
    task_id='wait_for_emr_step',
    job_flow_id='your_emr_cluster_id',  # Replace with your EMR cluster ID
    step_id="{{ task_instance.xcom_pull(task_ids='add_emr_steps', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag
)

# Define task dependencies
check_kafka_task >> add_emr_steps >> wait_for_emr_step
