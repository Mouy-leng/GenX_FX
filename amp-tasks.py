# AMP Task 2: Upload secrets to GitHub
import requests
import os
import sys

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable not set.")
    sys.exit(1)

REPO = 'Mouy-leng/GenX_FX'

secrets = {
    'BYBIT_API_KEY': 'your_bybit_key',
    'BYBIT_SECRET': 'your_bybit_secret', 
    'FXCM_USERNAME': 'your_fxcm_username',
    'FXCM_PASSWORD': 'your_fxcm_password',
    'GEMINI_API_KEY': 'your_gemini_key',
    'TELEGRAM_BOT_TOKEN': 'your_telegram_token'
}

print("AMP: Upload secrets to GitHub repository")
print("Run: python github-secrets-api.py")