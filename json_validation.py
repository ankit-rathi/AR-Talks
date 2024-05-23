import json
import jsonschema
from jsonschema import Draft7Validator

# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "format": "email"},
        "birthdate": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}$"
        }
    },
    "required": ["name", "age", "email", "birthdate"]
}

# Example JSON data
json_data = {
    "name": "John Doe",
    "age": -5,
    "email": "john.doe-at-email.com",
    "birthdate": "1990-13-01"
}

def validate_json(data, schema):
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    return errors

def capture_errors(errors):
    error_dict = {}
    for error in errors:
        error_path = '.'.join([str(elem) for elem in error.path]) or "root"
        if error_path not in error_dict:
            error_dict[error_path] = []
        error_dict[error_path].append(error.message)
    return error_dict

def main():
    # Validate the JSON data
    errors = validate_json(json_data, schema)
    
    if not errors:
        print("JSON is valid.")
    else:
        error_dict = capture_errors(errors)
        print("JSON is invalid. Found the following errors:")
        print(json.dumps(error_dict, indent=4))

if __name__ == "__main__":
    main()
