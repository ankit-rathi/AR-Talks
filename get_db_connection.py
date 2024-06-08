import boto3
import json
import psycopg2
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name):
    """
    Fetches a secret from AWS Secrets Manager and returns it as a JSON object.
    :param secret_name: The name of the secret.
    :param region_name: The region where the secret is stored.
    :return: A dictionary containing the secret.
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Fetch the secret value
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error fetching secret: {e}")
        return None

    # Parse the secret
    if 'SecretString' in response:
        secret = response['SecretString']
        return json.loads(secret)
    else:
        decoded_binary_secret = base64.b64decode(response['SecretBinary'])
        return json.loads(decoded_binary_secret)

def get_rds_connection(secret_name, region_name):
    """
    Establishes a connection to an AWS RDS database using credentials from Secrets Manager.
    :param secret_name: The name of the secret in Secrets Manager.
    :param region_name: The AWS region where the secret is stored.
    :return: A tuple containing the connection and cursor objects.
    """
    # Fetch the database configuration from Secrets Manager
    db_config = get_secret(secret_name, region_name)
    
    if not db_config:
        raise ValueError("Failed to retrieve database configuration from Secrets Manager")

    # Extract the database connection details
    dbname = db_config['dbname']
    user = db_config['username']
    password = db_config['password']
    host = db_config['host']
    port = db_config['port']

    # Establish the database connection
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Example usage
secret_name = "my-rds-secret"
region_name = "us-west-2"
connection, cursor = get_rds_connection(secret_name, region_name)

if connection and cursor:
    print("Successfully connected to the database")
    # Don't forget to close the connection and cursor when done
    cursor.close()
    connection.close()
else:
    print("Failed to connect to the database")
