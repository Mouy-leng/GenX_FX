import requests
import os
import sys

# This script updates a GitHub user profile and repository information.
# It has been updated to securely handle the GitHub token.

# --- Configuration ---
# The GitHub token should be loaded from an environment variable for security.
# Before running, set the token in your shell:
# export GITHUB_TOKEN='your_personal_access_token_here'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = 'Mouy-leng'


def print_error(message):
    """Prints an error message to stderr."""
    print(f"❌ Error: {message}", file=sys.stderr)


def print_success(message):
    """Prints a success message."""
    print(f"✅ {message}")


def main():
    """
    Main function to update GitHub profile and repository information.
    """
    # --- Pre-flight Check ---
    if not GITHUB_TOKEN:
        print_error("GITHUB_TOKEN environment variable is not set.")
        print("   Please set your GitHub Personal Access Token to run this script.")
        print("   Example: export GITHUB_TOKEN='ghp_...'")
        sys.exit(1)

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    # --- Update User Profile ---
    print("🔵 Updating user profile...")
    profile_data = {
        'blog': 'https://genx-fx.vercel.app',
        'company': 'GenX Trading Systems',
        'location': 'Cambodia',
        'bio': 'AI-Powered Forex Trading Platform Developer | GenX-FX Creator'
    }
    profile_url = 'https://api.github.com/user'

    try:
        response = requests.patch(profile_url, headers=headers, json=profile_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        print_success("Profile updated successfully.")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to update profile: {e}")
        if e.response is not None:
            print(f"   Response: {e.response.text}")

    # --- Update Repository Settings ---
    print("\n🔵 Updating repository information...")
    repo_data = {
        'homepage': 'https://genx-fx.vercel.app',
        'description': 'AI-Powered Forex Trading Platform with ML Predictions & Expert Advisors',
        'topics': ['forex', 'trading', 'ai', 'machine-learning', 'expert-advisor', 'mt4', 'mt5', 'python', 'react']
    }
    repo_url = f'https://api.github.com/repos/{USERNAME}/GenX_FX'

    try:
        repo_response = requests.patch(repo_url, headers=headers, json=repo_data)
        repo_response.raise_for_status()
        print_success("Repository updated successfully.")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to update repository: {e}")
        if e.response is not None:
            print(f"   Response: {e.response.text}")


if __name__ == "__main__":
    main()