import os

# This script creates a template for the .env file.
# It is a secure practice to avoid hardcoding secrets in the source code.

# .env content with placeholders
env_content = """
GITHUB_TOKEN=your_github_token
GITLAB_TOKEN=your_gitlab_token
CURSOR_CLI_API_KEY=your_cursor_api_key
AMP_TOKEN=your_amp_token
BYBIT_API_KEY=your_bybit_key
BYBIT_SECRET=your_bybit_secret
FXCM_USERNAME=your_fxcm_username
FXCM_PASSWORD=your_fxcm_password
GEMINI_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_BOT_TOKEN=your_discord_token
"""

# Write to .env.example, which is a safe, committable file
with open('.env.example', 'w') as f:
    f.write(env_content.strip())

print("Created .env.example with placeholder credentials.")
print("Please copy this file to .env and fill in your actual credentials.")