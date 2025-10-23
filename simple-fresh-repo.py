#!/usr/bin/env python3
"""
Simple fresh repository creation for GenX_FX
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd or "d:/GenX_FX_FRESH", capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_fresh_repo():
    fresh_path = Path("d:/GenX_FX_FRESH")
    
    print("Creating fresh repository...")
    
    # Create fresh directory
    fresh_path.mkdir(exist_ok=True)
    os.chdir(fresh_path)
    
    # Initialize git
    run_command("git init")
    run_command("git branch -M main")
    
    # Copy essential files only
    essential_files = [
        "main.py",
        "README.md", 
        ".gitignore",
        "requirements.txt",
        "maintain-repo.py",
        "maintain.bat",
        "sync-check.py"
    ]
    
    current_path = Path("d:/GenX_FX")
    
    for file_name in essential_files:
        src = current_path / file_name
        if src.exists():
            dest = fresh_path / file_name
            try:
                with open(src, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                with open(dest, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Copied: {file_name}")
            except Exception as e:
                print(f"Could not copy {file_name}: {e}")
    
    # Create basic structure
    (fresh_path / "core").mkdir(exist_ok=True)
    (fresh_path / "api").mkdir(exist_ok=True)
    (fresh_path / "expert-advisors").mkdir(exist_ok=True)
    (fresh_path / "config").mkdir(exist_ok=True)
    
    # Add and commit
    run_command("git add .")
    run_command('git commit -m "Clean GenX_FX repository - maintenance tools added"')
    
    # Add remote
    run_command("git remote add origin https://github.com/Mouy-leng/GenX_FX.git")
    
    print(f"Fresh repository created at: {fresh_path}")
    print("Ready to push!")

if __name__ == "__main__":
    create_fresh_repo()