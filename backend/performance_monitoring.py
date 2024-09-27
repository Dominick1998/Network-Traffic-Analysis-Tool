import psutil
import time

def get_cpu_usage():
    """
    Get the current CPU usage percentage.

    Returns:
        float: CPU usage as a percentage.
    """
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    """
    Get the current memory usage statistics.

    Returns:
        dict: Memory usage statistics including total, available, and percentage.
    """
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'percentage': memory.percent
    }

def track_response_time(start_time):
    """
    Calculate the response time for an API request.

    Args:
        start_time (float): The timestamp when the request started.

    Returns:
        float: The response time in seconds.
    """
    end_time = time.time()
    return end_time - start_time
