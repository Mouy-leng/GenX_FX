#!/usr/bin/env python3
"""
Complete GitHub Setup - Final step to ensure all secrets and variables are set
"""

import requests
import base64
from nacl import encoding, public
import os
import sys

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
REPO_OWNER = "Mouy-leng"
REPO_NAME = "GenX_FX"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

class GitHubSecretsManager:
    def __init__(self):
        if not GITHUB_TOKEN:
            print("Error: GITHUB_TOKEN environment variable not set.")
            sys.exit(1)
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_public_key(self):
        response = requests.get(f"{BASE_URL}/actions/secrets/public-key", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        raise Exception(f"Failed to get public key: {response.text}")
    
    def encrypt_secret(self, public_key_b64, secret_value):
        public_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
        box = public.SealedBox(public_key)
        encrypted = box.encrypt(secret_value.encode("utf-8"))
        return base64.b64encode(encrypted).decode("utf-8")
    
    def set_secret(self, name, value):
        key_data = self.get_public_key()
        encrypted_value = self.encrypt_secret(key_data["key"], value)
        data = {"encrypted_value": encrypted_value, "key_id": key_data["key_id"]}
        response = requests.put(f"{BASE_URL}/actions/secrets/{name}", headers=self.headers, json=data)
        return response.status_code in [201, 204]
    
    def set_variable(self, name, value):
        data = {"name": name, "value": value}
        response = requests.post(f"{BASE_URL}/actions/variables", headers=self.headers, json=data)
        return response.status_code in [201, 204]

def complete_setup():
    """Complete any missing secrets and variables"""
    manager = GitHubSecretsManager()
    
    print("Completing GitHub Setup...")
    print("=" * 30)
    
    # Additional secrets that might be missing
    secrets_to_check = {
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "MONGO_PASSWORD": os.getenv("MONGO_PASSWORD"),
        "REDIS_PASSWORD": os.getenv("REDIS_PASSWORD"),
        "FXCM_API_TOKEN": os.getenv("FXCM_API_TOKEN"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
    }

    additional_secrets = {k: v for k, v in secrets_to_check.items() if v}

    required_secrets = ["SECRET_KEY", "MONGO_PASSWORD", "REDIS_PASSWORD"]
    for secret in required_secrets:
        if secret not in additional_secrets:
            print(f"Error: Required environment variable {secret} is not set.")
            sys.exit(1)
    
    # Additional variables that might be missing
    additional_variables = {
        "NODE_ENV": "production",
        "LOG_LEVEL": "INFO",
        "PORT": "8000",
        "POSTGRES_DB": "genx_trading",
        "POSTGRES_USER": "genx_user",
        "REDIS_HOST": "redis",
        "REDIS_PORT": "6379"
    }
    
    print("\nSetting additional secrets...")
    for name, value in additional_secrets.items():
        try:
            success = manager.set_secret(name, value)
            print(f"   {'[OK]' if success else '[ERROR]'} {name}")
        except Exception as e:
            print(f"   [ERROR] {name}: {str(e)}")
    
    print("\nSetting additional variables...")
    for name, value in additional_variables.items():
        try:
            success = manager.set_variable(name, value)
            print(f"   {'[OK]' if success else '[ERROR]'} {name}")
        except Exception as e:
            print(f"   [ERROR] {name}: {str(e)}")
    
    print("\n[SUCCESS] Setup completion attempted!")

if __name__ == "__main__":
    complete_setup()