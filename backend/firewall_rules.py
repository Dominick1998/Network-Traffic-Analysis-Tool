import subprocess

def apply_firewall_rule(action, ip_address, port=None, protocol=None):
    """
    Apply a firewall rule to block or allow traffic based on the given parameters.

    Args:
        action (str): Action to take ('allow' or 'block').
        ip_address (str): IP address to apply the rule on.
        port (int): Optional, port to block or allow.
        protocol (str): Optional, protocol to block or allow (e.g., 'tcp', 'udp').

    Returns:
        dict: Success or failure message.
    """
    try:
        rule = f"sudo ufw {action} from {ip_address}"

        if port:
            rule += f" to any port {port}"
        
        if protocol:
            rule += f" proto {protocol}"

        subprocess.run(rule, shell=True, check=True)
        return {'message': f"Firewall rule '{action}' applied successfully for {ip_address}."}
    except subprocess.CalledProcessError as e:
        return {'error': f"Failed to apply firewall rule: {e}"}

def delete_firewall_rule(ip_address, port=None, protocol=None):
    """
    Remove a firewall rule for the given IP address.

    Args:
        ip_address (str): IP address to remove the rule from.
        port (int): Optional, port to remove the rule on.
        protocol (str): Optional, protocol to remove the rule on.

    Returns:
        dict: Success or failure message.
    """
    try:
        rule = f"sudo ufw delete deny from {ip_address}"

        if port:
            rule += f" to any port {port}"
        
        if protocol:
            rule += f" proto {protocol}"

        subprocess.run(rule, shell=True, check=True)
        return {'message': f"Firewall rule for {ip_address} removed successfully."}
    except subprocess.CalledProcessError as e:
        return {'error': f"
