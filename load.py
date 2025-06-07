# load.py
import subprocess
import sys
import os

def run(cmd, check=True):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

def main():
    # Pull the latest changes from GitHub
    run("git pull origin main")  # Adjust if you're not using 'main'

    # Warn if Python version doesn't match
    if os.path.exists(".python-version"):
        with open(".python-version") as f:
            required_version = f.read().strip()
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        if not current_version.startswith(required_version):
            print(f"⚠️ Warning: Required Python version is {required_version}, but you're using {current_version}.")

    # Install packages from requirements.txt
    if os.path.exists("requirements.txt"):
        run("pip install -r requirements.txt")
    else:
        print("requirements.txt not found.")

if __name__ == "__main__":
    main()
