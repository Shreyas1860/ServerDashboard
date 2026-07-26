import json
from pathlib import Path

status = json.loads(Path("status.json").read_text(encoding="utf-8"))

process_rows = "\n".join(
    f"| {p['name']} | {p['cpu']}% |"
    for p in status["top_processes"]
)

readme = f"""# 🖥️ Server Dashboard

## 🟢 Status

| Metric | Value |
|--------|-------|
| Hostname | {status["hostname"]} |
| Windows | {status["windows_version"]} |
| CPU | {status["cpu_percent"]}% |
| RAM | {status["memory"]["used_gb"]} / {status["memory"]["total_gb"]} GB ({status["memory"]["percent"]}%) |
| Disk | {status["disk"]["used_gb"]} / {status["disk"]["total_gb"]} GB ({status["disk"]["percent"]}%) |
| Uptime | {status["uptime"]["pretty"]} |
| Last Update | {status["last_update"]} |

---

## 🔥 Top Processes

| Process | CPU |
|---------|----:|
{process_rows}

---

Generated automatically from the server.
"""

Path("README.md").write_text(readme, encoding="utf-8")

print("README generated!")