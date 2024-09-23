import re

# Example text
text = "Your sample text with a 16-digit number like 1234567812345678 and another 2345678912345678."

# Function to mask the first 6 digits of a 16-digit number
def mask_number(match):
    # Get the matched 16-digit number
    number = match.group()
    # Mask the first 6 digits and keep the rest
    masked = 'X' * 6 + number[6:]
    return masked

# Use re.sub to substitute the 16-digit numbers with masked versions
masked_text = re.sub(r'\b\d{16}\b', mask_number, text)

print(masked_text)
