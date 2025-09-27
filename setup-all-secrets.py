import os

# This script sets up the .env file for the GenX FX trading platform.
# It is recommended to set these values as environment variables for security.
# This script will use placeholders if the environment variables are not found.

# Read credentials from environment variables, using placeholders as defaults
github_token = os.getenv('GITHUB_TOKEN', 'your_github_token_here')
gitlab_token = os.getenv('GITLAB_TOKEN', 'your_gitlab_token_here')
cursor_cli_api_key = os.getenv('CURSOR_CLI_API_KEY', 'your_cursor_cli_api_key_here')
amp_token = os.getenv('AMP_TOKEN', 'your_amp_token_here')

# Update .env file with all credentials
env_content = f"""
# --- GitHub and Development Tokens ---
# It is strongly recommended to set these as environment variables
# rather than writing them directly into this file.
GITHUB_TOKEN={github_token}
GITLAB_TOKEN={gitlab_token}
CURSOR_CLI_API_KEY={cursor_cli_api_key}
AMP_TOKEN={amp_token}

# --- Trading and Service API Keys (replace with your actual keys) ---
BYBIT_API_KEY=your_bybit_key_here
BYBIT_SECRET=your_bybit_secret_here
FXCM_USERNAME=your_fxcm_username_here
FXCM_PASSWORD=your_fxcm_password_here
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DISCORD_BOT_TOKEN=your_discord_bot_token_here
"""

with open('.env', 'w') as f:
    f.write(env_content.strip())

print("✅ .env file has been created/updated with credentials.")
print("ℹ️  Please ensure you replace placeholder values with your actual secrets.")
print("🔑 For production, it is recommended to manage these secrets using a secure vault or environment variables.")