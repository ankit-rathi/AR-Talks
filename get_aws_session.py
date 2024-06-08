import boto3
import configparser

def get_aws_session(config_file, profile='default'):
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(config_file)

    if profile not in config:
        raise ValueError(f"Profile {profile} not found in the config file")

    # Fetch the credentials and region from the config file
    aws_access_key_id = config[profile].get('aws_access_key_id')
    aws_secret_access_key = config[profile].get('aws_secret_access_key')
    region_name = config[profile].get('region')

    # Create a boto3 session
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return session

# Example usage
config_file = 'aws_config.ini'
session = get_aws_session(config_file)

# Verify the session by printing the current AWS identity
sts_client = session.client('sts')
identity = sts_client.get_caller_identity()
print(identity)
