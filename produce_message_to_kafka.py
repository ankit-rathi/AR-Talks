import boto3
import json
import base64
from botocore.exceptions import ClientError
from confluent_kafka import Producer
import configparser

def get_aws_session(config_file, profile='default'):
    """
    Fetches an AWS session based on a configuration file.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    if profile not in config:
        raise ValueError(f"Profile {profile} not found in the config file")

    aws_access_key_id = config[profile].get('aws_access_key_id')
    aws_secret_access_key = config[profile].get('aws_secret_access_key')
    region_name = config[profile].get('region')

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return session

def get_secret(session, secret_name, region_name):
    """
    Fetches a secret from AWS Secrets Manager and returns it as a JSON object.
    """
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error fetching secret: {e}")
        return None

    if 'SecretString' in response:
        secret = response['SecretString']
        return json.loads(secret)
    else:
        decoded_binary_secret = base64.b64decode(response['SecretBinary'])
        return json.loads(decoded_binary_secret)

def produce_message_to_kafka(topic, message, kafka_brokers, ssl_config):
    """
    Produces a JSON message to the specified Kafka topic using SSL configuration.
    """
    conf = {
        'bootstrap.servers': kafka_brokers,
        'security.protocol': 'SSL',
        'ssl.certificate.location': ssl_config['certificate'],
        'ssl.key.location': ssl_config['private_key'],
        'ssl.ca.location': ssl_config['ca_bundle']
    }

    producer = Producer(**conf)

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    producer.produce(topic, key=None, value=json.dumps(message), callback=delivery_report)
    producer.flush()

# Example usage
config_file = 'aws_config.ini'
profile = 'default'
secret_name = "my-ssl-certificates-secret"
region_name = "us-west-2"

# Get AWS session
session = get_aws_session(config_file, profile)

# Fetch SSL certificates from AWS Secrets Manager
ssl_certificates = get_secret(session, secret_name, region_name)

if ssl_certificates:
    kafka_brokers = 'your_kafka_broker:9093'
    topic = 'your_kafka_topic'
    message = {"key": "value"}  # Replace with your JSON message

    produce_message_to_kafka(topic, message, kafka_brokers, ssl_certificates)
else:
    print("Failed to fetch SSL certificates.")
