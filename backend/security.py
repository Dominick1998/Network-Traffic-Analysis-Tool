import re

def validate_ip_address(ip_address):
    """
    Validate the format of an IP address.

    Args:
        ip_address (str): The IP address to validate.

    Returns:
        bool: True if the IP address is valid, False otherwise.
    """
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(ip_pattern.match(ip_address))

def sanitize_input(input_string):
    """
    Sanitize input to prevent injection attacks.

    Args:
        input_string (str): The input string to sanitize.

    Returns:
        str: The sanitized string.
    """
    return re.sub(r'[^\w\s-]', '', input_string)
