import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    
    # Assuming you're passing a list of JSON strings
    parser.add_argument('json_args', nargs='+', help='List of JSON strings')
    
    args = parser.parse_args()
    
    # Process each JSON string
    for json_arg in args.json_args:
        try:
            json_obj = json.loads(json_arg)
            print(f"Parsed JSON object: {json_obj}")
            # Extract and use parameters as needed
            param1 = json_obj.get('param1')
            param2 = json_obj.get('param2')
            print(f"Parameter 1: {param1}")
            print(f"Parameter 2: {param2}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

if __name__ == "__main__":
    main()

{
    "applicationId": "your-application-id",
    "executionRoleArn": "your-execution-role-arn",
    "jobDriver": {
        "sparkSubmitJobDriver": {
            "entryPoint": "s3://your-bucket/your_script.py",
            "entryPointArguments": [
                "{\"param1\":\"value1\",\"param2\":\"value2\"}",
                "{\"param1\":\"value3\",\"param2\":\"value4\"}"
            ],
            "sparkSubmitParameters": "--conf spark.executor.memory=4g --conf spark.executor.cores=2"
        }
    },
    "configurationOverrides": {
        "monitoringConfiguration": {
            "s3MonitoringConfiguration": {
                "logUri": "s3://your-bucket/logs/"
            }
        }
    }
}
