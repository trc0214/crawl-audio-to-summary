import os
import subprocess

def run_scripts():
    venv_path = os.path.join(os.getcwd(), '.venv', 'Scripts', 'activate.bat')
    scripts = [
        "audio-to-summary/nas_crawer.py",
        "audio-to-summary/mp4-to-txt.py",
        "audio-to-summary/summarize.py"
    ]
    
    # Activate the virtual environment
    subprocess.run([venv_path], shell=True, check=True)
    
    for script in scripts:
        subprocess.run([".venv\\Scripts\\python", script], check=True)

if __name__ == "__main__":
    run_scripts()
