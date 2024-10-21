import json
import boto3
import os
import zipfile
from kafka import KafkaProducer
from kafka.errors import KafkaError

# S3 and Kafka configurations
S3_BUCKET_NAME = 'your-s3-bucket'
AWS_ACCESS_KEY = 'your-access-key'
AWS_SECRET_KEY = 'your-secret-key'
KAFKA_BROKER_URL = 'your-kafka-broker-url:9092'
KAFKA_TOPIC = 'unzipped_files_topic'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# 1. Read request body JSON for zip file names
def parse_request_body(request_body):
    try:
        request_data = json.loads(request_body)
        zip_files = request_data.get("zip_files", [])
        request_id = request_data.get("request_id", "default_request")
        return zip_files, request_id
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

# 2. Copy zip files from S3 bucket
def download_zip_files_from_s3(zip_files):
    local_zip_files = []
    for zip_file in zip_files:
        local_file_path = os.path.join("/tmp", zip_file)
        s3_client.download_file(S3_BUCKET_NAME, zip_file, local_file_path)
        local_zip_files.append(local_file_path)
        print(f"Downloaded {zip_file} to {local_file_path}")
    return local_zip_files

# 3. Unzip the files
def unzip_files(zip_files, request_id):
    unzipped_files = []
    for zip_file_path in zip_files:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            extract_path = os.path.dirname(zip_file_path)
            zip_ref.extractall(extract_path)
            for file_name in zip_ref.namelist():
                unzipped_files.append((file_name, zip_file_path, request_id))
        print(f"Unzipped {zip_file_path}")
    return unzipped_files

# 4. Rename unzipped files
def rename_unzipped_files(unzipped_files):
    renamed_files = []
    for file_name, zip_file_path, request_id in unzipped_files:
        original_file_path = os.path.join(os.path.dirname(zip_file_path), file_name)
        new_file_name = f"{request_id}_{os.path.basename(zip_file_path)}_{file_name}".replace(" ", "_")
        new_file_path = os.path.join(os.path.dirname(zip_file_path), new_file_name)
        os.rename(original_file_path, new_file_path)
        renamed_files.append(new_file_name)
        print(f"Renamed {original_file_path} to {new_file_name}")
    return renamed_files

# 5. Collate file names and send to Kafka topic
def send_file_names_to_kafka(renamed_files):
    try:
        producer.send(KAFKA_TOPIC, value={"files": renamed_files})
        producer.flush()
        print(f"Sent file names to Kafka topic: {KAFKA_TOPIC}")
    except KafkaError as e:
        print(f"Failed to send message to Kafka: {e}")

# 6. Delete zip files from S3
def delete_zip_files_from_s3(zip_files):
    try:
        for zip_file in zip_files:
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=zip_file)
            print(f"Deleted {zip_file} from S3 bucket {S3_BUCKET_NAME}")
    except Exception as e:
        print(f"Error deleting files from S3: {e}")

# Main workflow
def process_zip_files_workflow(request_body):
    try:
        # Step 1: Parse request body
        zip_files, request_id = parse_request_body(request_body)
        
        # Step 2: Download zip files from S3
        local_zip_files = download_zip_files_from_s3(zip_files)
        
        # Step 3: Unzip the files
        unzipped_files = unzip_files(local_zip_files, request_id)
        
        # Step 4: Rename the unzipped files
        renamed_files = rename_unzipped_files(unzipped_files)
        
        # Step 5: Send file names to Kafka
        send_file_names_to_kafka(renamed_files)
        
        # Step 6: Delete zip files from S3
        delete_zip_files_from_s3(zip_files)
        
        print("Process completed successfully!")

    except Exception as e:
        print(f"Error occurred during process: {e}")

