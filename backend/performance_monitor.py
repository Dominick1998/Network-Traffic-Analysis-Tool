import psutil
import time

def get_cpu_usage():
    """
    Get the current CPU usage percentage.

    Returns:
        dict: CPU usage percentage.
    """
    return {'cpu_usage': psutil.cpu_percent(interval=1)}

def get_memory_usage():
    """
    Get the current memory usage percentage.

    Returns:
        dict: Memory usage percentage.
    """
    memory_info = psutil.virtual_memory()
    return {
        'total_memory': memory_info.total,
        'available_memory': memory_info.available,
        'memory_usage': memory_info.percent
    }

def get_disk_usage():
    """
    Get the current disk usage percentage.

    Returns:
        dict: Disk usage percentage for each disk partition.
    """
    disk_usage = psutil.disk_partitions()
    usage_data = []
    for partition in disk_usage:
        usage = psutil.disk_usage(partition.mountpoint)
        usage_data.append({
            'partition': partition.device,
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        })
    return usage_data

def get_network_latency():
    """
    Simulate network latency measurement.

    Returns:
        dict: Network latency in milliseconds.
    """
    start_time = time.time()
    psutil.net_io_counters()
    end_time = time.time()
    latency = (end_time - start_time) * 1000  # convert to milliseconds
    return {'network_latency_ms': latency}
