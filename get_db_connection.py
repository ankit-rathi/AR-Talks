def get_rds_connection(config_file, secret_name, profile='default'):
    """
    Establishes a connection to an AWS RDS database using credentials from Secrets Manager.
    :param config_file: Path to the config file containing AWS credentials.
    :param secret_name: The name of the secret in Secrets Manager.
    :param profile: Profile name within the config file.
    :return: A tuple containing the connection and cursor objects.
    """
    session = get_aws_session(config_file, profile)
    db_config = get_secret(session, secret_name)
    
    if not db_config:
        raise ValueError("Failed to retrieve database configuration from Secrets Manager")

    dbname = db_config['dbname']
    user = db_config['username']
    password = db_config['password']
    host = db_config['host']
    port = db_config['port']

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
config_file = 'aws_config.ini'
secret_name = "my-rds-secret"
connection, cursor = get_rds_connection(config_file, secret_name)

if connection and cursor:
    print("Successfully connected to the database")
    # Don't forget to close the connection and cursor when done
    cursor.close()
    connection.close()
else:
    print("Failed to connect to the database")
