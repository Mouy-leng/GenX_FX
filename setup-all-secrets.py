import os

# This script provides a template for setting up your environment variables.
# It does NOT set them for you. You should create a `.env` file or
# set these environment variables in your system.

print("--- GenX FX Secrets Setup Guide ---")
print("Please create a file named '.env' in the root of the project and add the following lines:")
print("Replace 'your_..._here' with your actual credentials.\n")

env_example_content = """
# GitHub and other development tools
GITHUB_TOKEN=your_github_token_here
GITLAB_TOKEN=your_gitlab_token_here
CURSOR_CLI_API_KEY=your_cursor_cli_api_key_here
AMP_TOKEN=your_amp_token_here

# Trading Platforms
BYBIT_API_KEY=your_bybit_key_here
BYBIT_SECRET=your_bybit_secret_here
FXCM_USERNAME=your_fxcm_username_here
FXCM_PASSWORD=your_fxcm_password_here

# AI and Notification Services
GEMINI_API_KEY=your_gemini_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
DISCORD_BOT_TOKEN=your_discord_bot_token_here
"""

print(env_example_content)

print("\n--- Instructions ---")
print("1. Copy the content above into a new file named '.env'.")
print("2. Replace all placeholder values (e.g., 'your_github_token_here') with your actual secrets.")
print("3. Make sure the .env file is listed in your .gitignore to prevent it from being committed.")
print("\nSetup guide complete. Please create your .env file now.")