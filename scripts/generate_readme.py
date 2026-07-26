import json
from pathlib import Path

status = json.loads(Path("status.json").read_text(encoding="utf-8"))

process_rows = "\n".join(
    f"| {p['name']} | {p['cpu']}% |"
    for p in status["top_processes"]
)

readme = f"""# 🖥️ Server Dashboard

![Status](https://img.shields.io/badge/Status-Online-brightgreen)
![OS](https://img.shields.io/badge/Windows-Server-blue)
![Updated](https://img.shields.io/badge/Auto-Enabled-success)

---

## 📊 System Information

| Metric | Value |
|--------|-------|
| 🖥️ Hostname | {status["hostname"]} |
| 💻 Windows | {status["windows_version"]} |
| ⚙️ CPU Usage | {status["cpu_percent"]}% |
| 🧠 RAM Usage | {status["memory"]["used_gb"]} / {status["memory"]["total_gb"]} GB ({status["memory"]["percent"]}%) |
| 💾 Disk Usage | {status["disk"]["used_gb"]} / {status["disk"]["total_gb"]} GB ({status["disk"]["percent"]}%) |
| ⏱️ Uptime | {status["uptime"]["pretty"]} |
| 🕒 Last Update | {status["last_update"]} |

---

## 🔥 Top CPU Processes

| Process | CPU |
|---------|----:|
{process_rows}

---

### 🤖 About

This dashboard is generated automatically from a Windows server using **Python**, **Git**, and **GitHub Actions**.

_Last updated automatically._
"""

Path("README.md").write_text(readme, encoding="utf-8")

print("README generated successfully!")