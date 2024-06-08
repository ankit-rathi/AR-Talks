import boto3
import psycopg2  # Use pymysql if connecting to MySQL

def get_db_connection(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        # Fetch the secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        return None, None

    # Parse the secret (assume it's in JSON format)
    import json
    secret_dict = json.loads(secret)

    # Extract the required fields from the secret
    db_host = secret_dict['host']
    db_port = secret_dict['port']
    db_name = secret_dict['dbname']
    db_user = secret_dict['username']
    db_password = secret_dict['password']
    
    # Create a connection and cursor
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None, None

# Example usage
secret_name = "my_db_secret"
region_name = "us-west-2"
connection, cursor = get_db_connection(secret_name, region_name)

if connection and cursor:
    print("Successfully connected to the database.")
    # Perform database operations
    
    # Don't forget to close the connection and cursor when done
    cursor.close()
    connection.close()
else:
    print("Failed to connect to the database.")
