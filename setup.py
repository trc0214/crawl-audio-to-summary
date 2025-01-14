import os
import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def find_venv():
    possible_venvs = ['.venv', 'venv', 'env', 'ENV']
    for venv in possible_venvs:
        venv_path = os.path.join(os.getcwd(), venv, 'Scripts', 'python')
        if os.path.exists(venv_path):
            return venv_path
    return None

def run_scripts():
    # Ensure dotenv is installed
    install_package("python-dotenv")
    
    scripts = [
        "audio-to-summary/nas_crawer.py",
        "audio-to-summary/mp4-to-txt.py",
        "audio-to-summary/summarize.py"
    ]
    
    python_executable = find_venv() or sys.executable
    
    for script in scripts:
        subprocess.run([python_executable, script], check=True)

if __name__ == "__main__":
    run_scripts()
