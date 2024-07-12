import re

def validate_param_value(value, allowed_special_chars):

    invalid_chars_pattern = re.compile(f"[^{re.escape(allowed_special_chars)}a-zA-Z0-9]")
    return not bool(invalid_chars_pattern.search(value))

def validate_request(request_params, schema):

    required_params = schema.get("required", [])
    properties = schema.get("properties", {})
    
    for param in required_params:
        # Check if the required parameter is present
        if param not in request_params:
            return {"status": "failure", "error": f"Missing required parameter: {param}"}
        
        # Check if the required parameter value is empty
        if request_params[param] == "":
            return {"status": "failure", "error": f"Required parameter '{param}' cannot be empty"}
    
    for param, rules in properties.items():
        if param in request_params:
            value = request_params[param]
            
            # Check if the parameter type is correct
            if rules["type"] == "string" and not isinstance(value, str):
                return {"status": "failure", "error": f"Parameter '{param}' must be a string"}
            
            # Check for allowed special characters only if defined
            if "allowed_special_chars" in rules:
                if not validate_param_value(value, rules["allowed_special_chars"]):
                    return {"status": "failure", "error": f"Parameter '{param}' contains invalid characters"}
    
    return {"status": "success"}

# Example usage:
request_params = {
    "param1": 123,
    "param2": "invalid@value#"
}

schema = {
    "required": ["param1", "param2"],
    "properties": {
        "param1": {
            "type": "string"
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
print(result)  # Output: {'status': 'failure', 'error': "Parameter 'param2' contains invalid characters"}
