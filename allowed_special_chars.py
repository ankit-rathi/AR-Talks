import re

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
    schema (dict): JSON schema defining parameter types and allowed special characters.
    
    Returns:
    dict: Dictionary containing the validation status and error message if any check fails.
    """
    for param, rules in schema.items():
        # Check if the parameter is present in the request
        if param not in request_params:
            return {"status": "failure", "error": f"Missing required parameter: {param}"}
        
        value = request_params[param]
        
        # Check if the parameter type is correct
        if rules["type"] == "string" and not isinstance(value, str):
            return {"status": "failure", "error": f"Parameter '{param}' must be a string"}
        
        # Check for allowed special characters
        if not validate_param_value(value, rules["allowed_special_chars"]):
            return {"status": "failure", "error": f"Parameter '{param}' contains invalid characters"}
    
    return {"status": "success"}

schema = {
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


# Example usage:
request_params = {
    "param1": "valid_value-123",
    "param2": "invalid@value#",
    "param3": "another!valid$value%"
}

schema = {
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

result = validate_request(request_params, schema)
print(result)  # Output: {'status': 'success'}
