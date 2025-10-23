#!/usr/bin/env python3
"""
Create a fresh GenX_FX repository without secret history
"""

import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_fresh_repo():
    current_path = Path("d:/GenX_FX")
    backup_path = Path("d:/GenX_FX_OLD")
    fresh_path = Path("d:/GenX_FX_FRESH")
    
    print("Creating fresh repository without secrets...")
    
    # Step 1: Backup current repo
    if backup_path.exists():
        shutil.rmtree(backup_path)
    shutil.copytree(current_path, backup_path)
    print(f"Backup created at: {backup_path}")
    
    # Step 2: Create fresh directory
    if fresh_path.exists():
        shutil.rmtree(fresh_path)
    fresh_path.mkdir()
    
    # Step 3: Initialize new git repo
    os.chdir(fresh_path)
    run_command("git init")
    run_command("git branch -M main")
    
    # Step 4: Copy files excluding secrets and git history
    exclude_patterns = [
        ".git",
        "service-account-key.json",
        ".secrets",
        "aws-setup.bat",
        "update_all_secrets_real.py", 
        "clean_secrets.bat",
        "setup_github_security.bat",
        "sync_and_merge_guide.md",
        "__pycache__",
        "*.pyc",
        "node_modules",
        "GenX_FX_OLD",
        "GenX_FX_FRESH"
    ]
    
    def should_exclude(path):
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str or path.name == pattern:
                return True
        return False
    
    # Copy files
    for item in current_path.rglob('*'):
        if item.is_file() and not should_exclude(item):
            relative_path = item.relative_to(current_path)
            dest_path = fresh_path / relative_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(item, dest_path)
            except Exception as e:
                print(f"Could not copy {item}: {e}")
    
    print("Files copied to fresh repository")
    
    # Step 5: Create initial commit
    run_command("git add .")
    run_command('git commit -m "Initial commit: Clean GenX_FX repository without secrets"')
    
    # Step 6: Add remote
    run_command("git remote add origin https://github.com/Mouy-leng/GenX_FX.git")
    
    print(f"Fresh repository created at: {fresh_path}")
    print("Next steps:")
    print("1. cd d:/GenX_FX_FRESH")
    print("2. git push origin main --force")
    print("3. If successful, replace d:/GenX_FX with d:/GenX_FX_FRESH")

if __name__ == "__main__":
    create_fresh_repo()