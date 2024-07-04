import functools

def log_function_details(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        print(f"Module Name: {module_name}")
        print(f"Function Name: {func.__name__}")
        print(f"Input Parameters: args: {args}, kwargs: {kwargs}")
        
        result = func(*args, **kwargs)
        
        print(f"Output: {result}")
        return result
    
    return wrapper

# Example usage
@log_function_details
def add(a, b):
    return a + b

add(5, 3)
