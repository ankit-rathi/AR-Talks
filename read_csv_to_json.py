import boto3
import pandas as pd
import io

# Initialize the S3 client
s3 = boto3.client('s3')

# Function to read a CSV from S3 and convert to JSON
def csv_to_json_from_s3(bucket_name, file_key):
    try:
        # Get the CSV file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the CSV content from the response body
        csv_content = response['Body'].read().decode('utf-8')
        
        # Convert the CSV content to a pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Convert the DataFrame to JSON with CSV headers as keys
        json_output = df.to_json(orient='records')
        
        print(f"JSON Output: {json_output}")
        return json_output

    except Exception as e:
        print(f"Error reading the CSV file from S3: {e}")

# Example usage
bucket_name = 'your-bucket-name'
file_key = 'path/to/your-csv-file.csv'

csv_to_json_from_s3(bucket_name, file_key)
