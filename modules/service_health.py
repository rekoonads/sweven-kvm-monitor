import os
import time
from modules import logger

def collect_data():
    """Collect service health metrics"""
    try:
        # Service uptime (time since container started)
        uptime_seconds = time.time() - psutil.boot_time()

        data = {
            'host': os.getenv('RAILWAY_SERVICE_NAME', 'unknown'),
            'service_name': os.getenv('RAILWAY_SERVICE_NAME', 'kvm-monitor'),
            'environment': os.getenv('RAILWAY_ENVIRONMENT', 'production'),
            'region': os.getenv('RAILWAY_REGION', 'unknown'),
            'uptime_seconds': uptime_seconds,
            'uptime_hours': uptime_seconds / 3600,
            'status': 'healthy',
        }

        return data
    except Exception as e:
        logger.error(f"Error collecting service health: {e}")
        return None

import psutil
