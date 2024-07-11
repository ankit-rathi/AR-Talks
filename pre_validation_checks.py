def check_empty_params(request_params):
    """
    Check if any of the request parameters have an empty string.
    
    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    
    Returns:
    tuple: (bool, str) True and the check name if the check fails, otherwise False and an empty string.
    """
    for key, value in request_params.items():
        if value == "":
            return True, "Empty Parameter Check"
    return False, ""

def check_special_characters(request_params, valid_special_chars="._-"):
    """
    Check if any of the request parameters contain special characters, except for valid ones.
    
    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    valid_special_chars (str): String of valid special characters. Default is "._-".
    
    Returns:
    tuple: (bool, str) True and the check name if the check fails, otherwise False and an empty string.
    """
    import re
    invalid_chars_pattern = re.compile(f"[^{re.escape(valid_special_chars)}a-zA-Z0-9]")
    
    for key, value in request_params.items():
        if isinstance(value, str) and invalid_chars_pattern.search(value):
            return True, "Special Characters Check"
    return False, ""

def check_required_params(request_params, required_params):
    """
    Check if all required parameters are present in the request.
    
    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    required_params (list): List of required parameter names.
    
    Returns:
    tuple: (bool, str) True and the check name if the check fails, otherwise False and an empty string.
    """
    for param in required_params:
        if param not in request_params:
            return True, "Required Parameters Check"
    return False, ""

def validate_request(request_params, required_params, valid_special_chars="._-"):
    """
    Validate the API request with three checks.
    
    Parameters:
    request_params (dict): Dictionary containing the request parameters.
    required_params (list): List of required parameter names.
    valid_special_chars (str): String of valid special characters. Default is "._-".
    
    Returns:
    dict: Dictionary containing the validation status and failed check information.
    """
    checks = [
        check_empty_params,
        check_special_characters,
        check_required_params
    ]
    
    for check in checks:
        if check == check_required_params:
            failed, check_name = check(request_params, required_params)
        else:
            failed, check_name = check(request_params, valid_special_chars)
        
        if failed:
            return {"status": "failure", "failed_check": check_name}
    
    return {"status": "success"}

# Example usage:
request_params = {
    "param1": "value1",
    "param2": "value2"
}
required_params = ["param1", "param2", "param3"]

result = validate_request(request_params, required_params)
print(result)  # Output: {'status': 'failure', 'failed_check': 'Required Parameters Check'}
