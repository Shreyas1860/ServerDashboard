import json
import platform
import socket
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


def get_uptime():
    boot = psutil.boot_time()
    uptime = int(time.time() - boot)

    days = uptime // 86400
    hours = (uptime % 86400) // 3600
    minutes = (uptime % 3600) // 60

    return {
        "seconds": uptime,
        "pretty": f"{days}d {hours}h {minutes}m"
    }


def get_top_processes(limit=5):
    processes = []

    # Prime CPU counters
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except Exception:
            pass

    time.sleep(1)

    for p in psutil.process_iter(["pid", "name"]):
        try:
            processes.append({
                "pid": p.info["pid"],
                "name": p.info["name"],
                "cpu": p.cpu_percent(None)
            })
        except Exception:
            pass

    processes.sort(key=lambda x: x["cpu"], reverse=True)
    return processes[:limit]


status = {
    "hostname": socket.gethostname(),
    "windows_version": platform.platform(),
    "last_update": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),

    "cpu_percent": psutil.cpu_percent(interval=1),

    "memory": {
        "percent": psutil.virtual_memory().percent,
        "used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    },

    "disk": {
        "percent": psutil.disk_usage("/").percent,
        "used_gb": round(psutil.disk_usage("/").used / (1024**3), 2),
        "total_gb": round(psutil.disk_usage("/").total / (1024**3), 2),
    },

    "uptime": get_uptime(),

    "top_processes": get_top_processes(),
}

Path("status.json").write_text(
    json.dumps(status, indent=4),
    encoding="utf-8"
)

print("status.json updated successfully!")