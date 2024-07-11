def check_empty_params(request_params):
    """
    Check if any of the request parameters have an empty string.

    Parameters:
    request_params (dict): Dictionary containing the request parameters.

    Returns:
    bool: True if any parameter is an empty string, False otherwise.
    """
    empty_keys = []
    for key, value in request_params.items():
        if value == "":
            empty_keys.append(key)
    return empty_keys

# Example usage:
params = {
    "param1": "value1",
    "param2": "value2",
    "param3": "value3"
}

print(check_empty_params(params))  # Output: True
