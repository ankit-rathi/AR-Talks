import boto3
import json
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

# Example usage
secret_name = "my-secret-name"
region_name = "us-west-2"
secret = get_secret(secret_name, region_name)

if secret:
    print("Fetched secret:", secret)
else:
    print("Failed to fetch secret.")
