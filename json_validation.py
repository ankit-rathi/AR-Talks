def get_hierarchy_level(json_obj):
    def _get_level(obj, level):
        if isinstance(obj, dict):
            if not obj:
                return level
            return max(_get_level(v, level + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return level
            return max(_get_level(v, level + 1) for v in obj)
        else:
            return level

    return _get_level(json_obj, 0)

# Example usage:
import json

# Sample JSON object
json_data = {
    "key1": {
        "key2": 
            "abc"
        
    }
}

# Convert the JSON object to a Python dictionary
dict_data = json.loads(json.dumps(json_data))

# Get the hierarchy level
level = get_hierarchy_level(dict_data)
print("Hierarchy level:", level)


import json
import jsonschema
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

# Define the JSON schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "format": "email"},
        "birthdate": {
            "type": "string",
            "pattern": r"^\d{4}-\d{2}-\d{2}$",
            "errorMessage": {
                "pattern": "Birthdate must be in YYYY-MM-DD format."
            }
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

def main():
    # Validate the JSON data
    errors = validate_json(json_data, schema)
    
    if not errors:
        print("JSON is valid.")
    else:
        print("JSON is invalid. Found the following errors:")
        for error in errors:
            print(f" - {error.message}")

if __name__ == "__main__":
    main()

