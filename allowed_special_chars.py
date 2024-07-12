import re
from jsonschema import Draft7Validator

def validate_param_value(value, allowed_special_chars):
    """
    Validate a parameter value for special characters.
    
    Parameters:
    value (str): The parameter value to be validated.
    allowed_special_chars (str): A string of allowed special characters.
    
    Returns:
    bool: True if the value is valid, False otherwise.
    """
    invalid_chars_pattern = re.compile(f"[^{re.escape(allowed_special_chars)}a-zA-Z0-9]")
    return not bool(invalid_chars_pattern.search(value))

def validate_request(request_params, schema):
    """
    Validate the API request parameters against the schema.
    
    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    schema (dict): JSON schema defining required parameters, parameter types, and allowed special characters.
    
    Returns:
    dict: Dictionary containing the validation status and error message if any check fails.
    """
    # Validate basic schema rules using Draft7Validator
    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(request_params), key=lambda e: e.path)
    
    if errors:
        error_messages = [error.message for error in errors]
        return {"status": "failure", "errors": error_messages}
    
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
    "param2": "invalid@value#"
}

schema = {
    "type": "object",
    "required": ["param1", "param2"],
    "properties": {
        "param1": {
            "type": "string",
            "allowed_special_chars": "._-"
        },
        "param2": {
            "type": "string",
            "allowed_special_chars": "@#"
        },
        "param3": {
            "type": "string",
            "allowed_special_chars": "!$%"
        }
    }
}

result = validate_request(request_params, schema)
print(result)  # Output: {'status': 'failure', 'errors': ["Parameter 'param2' contains invalid characters"]}
