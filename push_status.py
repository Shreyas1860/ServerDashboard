from git import Repo
import subprocess
import sys
from pathlib import Path

REPO_PATH = Path(__file__).parent

# Generate a fresh status.json
result = subprocess.run([sys.executable, "status.py"], cwd=REPO_PATH)

if result.returncode != 0:
    raise RuntimeError("status.py failed")

repo = Repo(REPO_PATH)

# Stage status.json
repo.index.add(["status.json"])

# Commit only if something changed
if repo.is_dirty(index=True, working_tree=True):
    repo.index.commit("Update server status")
    origin = repo.remote(name="origin")
    origin.push()
    print("✅ Changes pushed to GitHub!")
else:
    print("ℹ️ No changes to push.")