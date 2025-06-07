import subprocess
import sys

def run(cmd, check=True):
    """
    Runs a shell command, prints output, and optionally checks for failure.
    
    Args:
        cmd (str): Command to run.
        check (bool): Whether to raise an error if the command fails.
    """
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    
    if check and result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)

def main():
    # Ensure the user provided a commit message
    if len(sys.argv) < 2:
        print("Usage: python save.py \"Your commit message here\"")
        sys.exit(1)

    commit_message = sys.argv[1]

    # Save current Python dependencies to requirements.txt
    run("pip freeze > requirements.txt")

    # Save current Python version to .python-version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    with open(".python-version", "w") as f:
        f.write(python_version + "\n")

    # Stage all changes in the repository
    run("git add .")

    # Commit with the user's message
    run(f'git commit -m "{commit_message}"', check=False)

    # Push the changes to the remote repository (default branch: main)
    run("git push origin main")

if __name__ == "__main__":
    main()
