import boto3
import json
import base64
from botocore.exceptions import ClientError
from confluent_kafka import Producer

def get_secret(secret_name, region_name):
    """
    Fetches a secret from AWS Secrets Manager and returns it as a JSON object.
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

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
