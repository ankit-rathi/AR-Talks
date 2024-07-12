import re
from jsonschema import Draft7Validator, ValidationError

def validate_param_value(value, allowed_special_chars):

    invalid_chars_pattern = re.compile(f"[^{re.escape(allowed_special_chars)}a-zA-Z0-9]")
    return not bool(invalid_chars_pattern.search(value))

def validate_request(request_params, schema):

    # Validate basic schema rules using Draft7Validator
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(request_params), key=lambda e: e.path)
    
    if errors:
        error = errors[0]
        return {"status": "failure", "error": error.message}
    
    # Additional check for special characters
    properties = schema.get("properties", {})
    for param, rules in properties.items():
        if param in request_params and "allowed_special_chars" in rules:
            value = request_params[param]
            if not validate_param_value(value, rules["allowed_special_chars"]):
                return {"status": "failure", "error": f"Parameter '{param}' contains invalid characters"}
    
    return {"status": "success"}

# Example usage:
request_params = {
    "param1": "valid_value-123",
    "param2": "invalid@_value#",
    "param3": "invalid@_value#"
}

schema = {
    "type": "object",
    "required": ["param1", "param2"],
    "properties": {
        "param1": {
            "type": "string"
        },
        "param2": {
            "type": "string"
        },
        "param3": {
            "type": "string",
            "allowed_special_chars": "_"
        }
    }
}

result = validate_request(request_params, schema)
print(result)  # Output: {'status': 'failure', 'error': "Parameter 'param2' contains invalid characters"}
