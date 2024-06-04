from kafka import KafkaProducer
import boto3
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from datetime import datetime, timedelta

# Function to write a message to AWS Kafka topic
def write_to_kafka(topic, message):
    producer = KafkaProducer(bootstrap_servers='b-1.exampleClusterId.kafka.amazonaws.com:9092', security_protocol='SSL', ssl_cafile='/path/to/ca.pem', ssl_certfile='/path/to/service.cert', ssl_keyfile='/path/to/service.key')
    producer.send(topic, message.encode())
    producer.flush()

# Function to check unconsumed messages in AWS Kafka topic
def check_kafka_lag():
    client = boto3.client('kafka', region_name='us-east-1')
    response = client.get_bootstrap_brokers(ClusterArn='arn:aws:kafka:us-east-1:YOUR_ACCOUNT_ID:cluster/YOUR_CLUSTER_NAME/YOUR_CLUSTER_ID')
    bootstrap_servers = response['BootstrapBrokerString']
    consumer = KafkaConsumer(
        'your_kafka_topic',
        bootstrap_servers=bootstrap_servers,
        security_protocol='SSL',
        ssl_cafile='/path/to/ca.pem',
        ssl_certfile='/path/to/service.cert',
        ssl_keyfile='/path/to/service.key'
    )
    lag = 0
    for partition in consumer.partitions_for_topic('your_kafka_topic'):
        tp = TopicPartition('your_kafka_topic', partition)
        consumer.assign([tp])
        consumer.seek_to_end(tp)
        latest_offset = consumer.position(tp)
        committed_offset = consumer.committed(tp)
        if committed_offset is None:
            committed_offset = 0
        partition_lag = latest_offset - committed_offset
        lag += partition_lag
        print(f'Partition {partition} lag: {partition_lag}')
    consumer.close()
    print(f'Total lag: {lag}')
    return lag

# Function to trigger EMR job for unconsumed messages to write into RDS
def trigger_emr_for_unconsumed_messages():
    client = boto3.client('emr', region_name='us-east-1')
    step = {
        'Name': 'WriteToRDSStep',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode',
                'cluster',
                's3://your-bucket/your-script.py',
                'your_rds_endpoint',
                'your_rds_username',
                'your_rds_password',
                'your_rds_database'
            ]
        }
    }
    response = client.add_job_flow_steps(JobFlowId='your_emr_cluster_id', Steps=[step])
    return response['StepIds'][0]

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'kafka_to_emr_to_rds',
    default_args=default_args,
    description='A DAG to write message to Kafka, check Kafka lag, and trigger EMR job to write to RDS',
    schedule_interval=timedelta(days=1),
)

# Define tasks
start_task = DummyOperator(task_id='start_task', dag=dag)
emr_step_task = EmrAddStepsOperator(
    task_id='add_emr_step',
    job_flow_id='YOUR_EMR_CLUSTER_ID',
    aws_conn_id='aws_default',
    steps=[
        {
            'Name': 'WriteToRDSStep',
            'ActionOnFailure': 'CONTINUE',
            'HadoopJarStep': {
                'Jar': 'command-runner.jar',
                'Args': ['echo', 'Hello World']
            }
        }
    ],
    dag=dag
)

# Set task dependencies
start_task >> emr_step_task



from kafka import KafkaProducer
from kafka.errors import KafkaError

# Kafka configuration
conf = {
    'bootstrap_servers': 'your.kafka.broker:port',
    'security_protocol': 'SSL',
    'ssl_cafile': '/path/to/ca-cert',         # Path to CA certificate
    'ssl_certfile': '/path/to/cert',          # Path to client's public certificate
    'ssl_keyfile': '/path/to/key',            # Path to client's private key
    'ssl_password': 'your_key_password',      # Password for the client's private key, if needed
}

# Create the KafkaProducer instance
producer = KafkaProducer(**conf)

# Topic and message
topic = 'your_topic'
message = 'Hello, Kafka with SSL!'

# Produce the message
future = producer.send(topic, value=message.encode('utf-8'))

try:
    # Wait for send to complete
    record_metadata = future.get(timeout=10)
    print(f'Message delivered to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}')
except KafkaError as e:
    print(f'Message delivery failed: {e}')
finally:
    # Close the producer
    producer.close()

