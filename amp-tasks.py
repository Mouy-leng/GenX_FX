# AMP Task 2: Define secrets for GitHub upload
import os

# It is recommended to set the GITHUB_TOKEN as an environment variable
# for security reasons, rather than hardcoding it.
# Example: export GITHUB_TOKEN='your_github_personal_access_token'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'Mouy-leng'
REPO_NAME = 'GenX_FX'

# This script defines the secrets that should be uploaded to the GitHub repository.
# The actual upload is handled by other scripts, like 'github-secrets-api.py'.
# The values here are placeholders and should be replaced by actual secrets
# in a secure manner, for example, by sourcing them from a secure vault or a local .env file.
secrets_to_upload = {
    'BYBIT_API_KEY': 'your_bybit_key_here',
    'BYBIT_SECRET': 'your_bybit_secret_here',
    'FXCM_USERNAME': 'your_fxcm_username_here',
    'FXCM_PASSWORD': 'your_fxcm_password_here',
    'GEMINI_API_KEY': 'your_gemini_api_key_here',
    'TELEGRAM_BOT_TOKEN': 'your_telegram_bot_token_here'
}

def main():
    """
    Main function to check for the GitHub token and provide instructions.
    """
    print("✅ AMP Task: Define secrets for GitHub repository")

    if not GITHUB_TOKEN:
        print("\n⚠️  Warning: GITHUB_TOKEN environment variable is not set.")
        print("   Please set it to a valid GitHub Personal Access Token with 'repo' scope.")
        print("   Example: export GITHUB_TOKEN='ghp_...'")
    else:
        print("\n✅ GITHUB_TOKEN is set.")

    print("\nℹ️  This script defines the list of secrets to be uploaded.")
    print(f"   Secrets to be set for repository: {REPO_OWNER}/{REPO_NAME}")
    for secret_name in secrets_to_upload:
        print(f"     - {secret_name}")

    print("\n🚀 To perform the actual upload, run a dedicated secrets management script, such as:")
    print("   python github-secrets-manager.py")


if __name__ == "__main__":
    main()