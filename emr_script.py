import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('--json_args', type=str, required=True, help='JSON string of arguments')
    
    args = parser.parse_args()
    
    # Parse the JSON string
    json_args = json.loads(args.json_args)
    
    # Use the parameters from the JSON
    param1 = json_args.get('param1')
    param2 = json_args.get('param2')
    
    print(f"Parameter 1: {param1}")
    print(f"Parameter 2: {param2}")

if __name__ == "__main__":
    main()

{
    "applicationId": "your-application-id",
    "executionRoleArn": "your-execution-role-arn",
    "jobDriver": {
        "sparkSubmitJobDriver": {
            "entryPoint": "s3://your-bucket/your_script.py",
            "entryPointArguments": ["--json_args", "{\"param1\":\"value1\",\"param2\":\"value2\"}"],
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
