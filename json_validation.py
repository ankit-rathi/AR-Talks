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

import jsonschema
from jsonschema import Draft7Validator, FormatChecker
from datetime import datetime

# Define a custom format checker function for strict date format
def is_valid_date(instance):
    try:
        datetime.strptime(instance, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Register the custom format checker for the 'date' format
format_checker = FormatChecker()
format_checker.checks('date')(is_valid_date)

# Define your JSON schema with the desired date format
schema = {
    "type": "object",
    "properties": {
        "date": {"type": "string", "format": "date"}
    },
    "required": ["date"]
}

# Create a JSON object to validate against the schema
data = {
    "date": "20-05-30"
}

# Create a validator with the schema and format checker
validator = Draft7Validator(schema, format_checker=format_checker)
errors = validator.iter_errors(data)

# Iterate over any validation errors and print them
for error in errors:
    print(error.message)

