import psutil
import os
from modules import logger

def collect_data():
    """Collect container-specific resource metrics"""
    try:
        # Get current process (container)
        process = psutil.Process(os.getpid())

        # CPU and memory for the container
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        # Container-specific metrics
        data = {
            'host': os.getenv('RAILWAY_SERVICE_NAME', 'unknown'),
            'cpu_percent': cpu_percent,
            'cpu_count': psutil.cpu_count(),
            'memory_percent': memory.percent,
            'memory_used_mb': memory.used / (1024 * 1024),
            'memory_available_mb': memory.available / (1024 * 1024),
            'memory_total_mb': memory.total / (1024 * 1024),
            'process_count': len(psutil.pids()),
        }

        return data
    except Exception as e:
        logger.error(f"Error collecting container stats: {e}")
        return None
