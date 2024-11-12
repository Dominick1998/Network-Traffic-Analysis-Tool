# backend/firewall_management.py

import subprocess
import platform
from backend.database import get_db_session
from backend.models import FirewallRule
from datetime import datetime

def get_firewall_rules():
    """
    Get a list of current firewall rules from both the system and database.

    Returns:
        list: A combined list of system and database-stored firewall rules.
    """
    system_rules = []
    system = platform.system()

    # Fetch firewall rules based on the operating system
    if system == "Linux":
        result = subprocess.run(['sudo', 'iptables', '-L'], stdout=subprocess.PIPE)
        system_rules = result.stdout.decode('utf-8').splitlines()
    elif system == "Windows":
        result = subprocess.run(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'], stdout=subprocess.PIPE)
        system_rules = result.stdout.decode('utf-8').splitlines()

    # Fetch additional database-stored firewall rules
    session = get_db_session()
    try:
        db_rules = session.query(FirewallRule).all()
        db_rules_list = [{'rule': rule.rule, 'created_at': rule.created_at.isoformat()} for rule in db_rules]
    finally:
        session.close()

    return {
        'system_rules': system_rules,
        'db_rules': db_rules_list
    }

def add_firewall_rule(rule):
    """
    Add a new firewall rule to both the system and the database.

    Args:
        rule (str): The firewall rule to add.

    Returns:
        dict: Success or failure message.
    """
    system = platform.system()

    try:
        # Apply rule at system level
        if system == "Linux":
            subprocess.run(['sudo', 'iptables', '-A'] + rule.split(), check=True)
        elif system == "Windows":
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule'] + rule.split(), check=True)
        else:
            return {'error': 'Unsupported system'}

        # Log rule in the database
        session = get_db_session()
        new_rule = FirewallRule(rule=rule, created_at=datetime.utcnow())
        session.add(new_rule)
        session.commit()

        return {'message': 'Firewall rule added successfully.'}
    except subprocess.CalledProcessError as e:
        return {'error': f"Failed to add firewall rule: {e}"}
    finally:
        session.close()

def delete_firewall_rule(rule):
    """
    Delete an existing firewall rule from both the system and the database.

    Args:
        rule (str): The firewall rule to delete.

    Returns:
        dict: Success or failure message.
    """
    system = platform.system()

    try:
        # Remove rule at system level
        if system == "Linux":
            subprocess.run(['sudo', 'iptables', '-D'] + rule.split(), check=True)
        elif system == "Windows":
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'delete', 'rule'] + rule.split(), check=True)
        else:
            return {'error': 'Unsupported system'}

        # Remove rule from the database
        session = get_db_session()
        db_rule = session.query(FirewallRule).filter_by(rule=rule).first()
        if db_rule:
            session.delete(db_rule)
            session.commit()
            return {'message': 'Firewall rule deleted successfully from system and database.'}
        else:
            return {'error': 'Firewall rule not found in database.'}
    except subprocess.CalledProcessError as e:
        return {'error': f"Failed to delete firewall rule: {e}"}
    finally:
        session.close()
