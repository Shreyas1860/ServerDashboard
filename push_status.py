from git import Repo, GitCommandError
import subprocess
import sys
from pathlib import Path
import json

REPO_PATH = Path(__file__).parent

# ---------------------------------
# Generate status.json
# ---------------------------------

result = subprocess.run(
    [sys.executable, "status.py"],
    cwd=REPO_PATH
)

if result.returncode != 0:
    raise RuntimeError("status.py failed")

# ---------------------------------
# Update history.json
# ---------------------------------

status_file = REPO_PATH / "status.json"
history_file = REPO_PATH / "history.json"

status = json.loads(status_file.read_text(encoding="utf-8"))

if history_file.exists():
    history = json.loads(history_file.read_text(encoding="utf-8"))
else:
    history = []

history.append({
    "time": status["last_update"],
    "cpu": status["cpu_percent"],
    "ram": status["memory"]["percent"],
    "disk": status["disk"]["percent"]
})

# Keep only latest 200 entries
history = history[-200:]

history_file.write_text(
    json.dumps(history, indent=4),
    encoding="utf-8"
)

# ---------------------------------
# Git
# ---------------------------------

repo = Repo(REPO_PATH)
origin = repo.remote("origin")

# Stage files
repo.index.add([
    "status.json",
    "history.json"
])

# Check whether anything is actually staged
if repo.index.diff("HEAD"):
    try:
        # Commit local changes
        repo.index.commit("Update server status")

        # Rebase onto latest remote commit
        print("Pulling latest changes...")
        origin.pull(rebase=True)

        # Push local commit
        print("Pushing changes...")
        origin.push()

        print("✅ Changes pushed to GitHub!")

    except GitCommandError as e:
        print(f"❌ Git command failed:\n{e}")

    except Exception as e:
        print(f"❌ Unexpected error:\n{e}")

else:
    print("ℹ️ No changes detected.")