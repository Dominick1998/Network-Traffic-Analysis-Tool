import subprocess
import platform

def get_firewall_rules():
    """
    Get a list of current firewall rules.

    Returns:
        list: A list of firewall rules.
    """
    system = platform.system()

    if system == "Linux":
        # Fetch firewall rules on Linux using iptables
        result = subprocess.run(['sudo', 'iptables', '-L'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').splitlines()
    elif system == "Windows":
        # Fetch firewall rules on Windows using netsh
        result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'], stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').splitlines()
    else:
        return []

def add_firewall_rule(rule):
    """
    Add a new firewall rule.

    Args:
        rule (str): The rule to add.

    Returns:
        dict: Success or failure message.
    """
    system = platform.system()

    if system == "Linux":
        try:
            subprocess.run(['sudo', 'iptables', '-A', rule], check=True)
            return {'message': 'Firewall rule added successfully.'}
        except subprocess.CalledProcessError as e:
            return {'error': f"Failed to add firewall rule: {e}"}
    elif system == "Windows":
        try:
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', rule], check=True)
            return {'message': 'Firewall rule added successfully.'}
        except subprocess.CalledProcessError as e:
            return {'error': f"Failed to add firewall rule: {e}"}
    else:
        return {'error': 'Unsupported system'}

def delete_firewall_rule(rule):
    """
    Delete an existing firewall rule.

    Args:
        rule (str): The rule to delete.

    Returns:
        dict: Success or failure message.
    """
    system = platform.system()

    if system == "Linux":
        try:
            subprocess.run(['sudo', 'iptables', '-D', rule], check=True)
            return {'message': 'Firewall rule deleted successfully.'}
        except subprocess.CalledProcessError as e:
            return {'error': f"Failed to delete firewall rule: {e}"}
    elif system == "Windows":
        try:
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule', rule], check=True)
            return {'message': 'Firewall rule deleted successfully.'}
        except subprocess.CalledProcessError as e:
            return {'error': f"Failed to delete firewall rule: {e}"}
    else:
        return {'error': 'Unsupported system'}
