import psutil

def get_system_health():
    """
    Retrieve the current system health metrics, including CPU, memory, disk, and network activity.

    Returns:
        dict: System health metrics.
    """
    health_data = {
        'cpu_usage': psutil.cpu_percent(interval=1),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent,
        'network_sent': psutil.net_io_counters().bytes_sent,
        'network_received': psutil.net_io_counters().bytes_recv,
    }
    return health_data
