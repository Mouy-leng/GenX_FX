import requests
import os
import sys

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    print("Error: GITHUB_TOKEN environment variable is not set.", file=sys.stderr)
    sys.exit(1)

USERNAME = 'Mouy-leng'

# Update user profile
profile_data = {
    'blog': 'https://genxfx.org',
    'company': 'A6..9V',
    'location': 'Phnompenh, Battambang, Cambodia',
    'bio': 'Developer'
}

url = f'https://api.github.com/user'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.patch(url, headers=headers, json=profile_data)

if response.status_code == 200:
    print("Profile updated successfully")
else:
    print(f"Error updating profile: {response.status_code}", file=sys.stderr)
    print(response.text, file=sys.stderr)


# Update repository settings
repo_data = {
    'homepage': 'https://genx-fx.vercel.app',
    'description': 'AI-Powered Forex Trading Platform with ML Predictions & Expert Advisors',
    'topics': ['forex', 'trading', 'ai', 'machine-learning', 'expert-advisor', 'mt4', 'mt5']
}

repo_url = f'https://api.github.com/repos/{USERNAME}/GenX_FX'
repo_response = requests.patch(repo_url, headers=headers, json=repo_data)

if repo_response.status_code == 200:
    print("Repository updated successfully")
else:
    print(f"Error updating repository: {repo_response.status_code}", file=sys.stderr)
    print(repo_response.text, file=sys.stderr)

# If either request failed, exit with an error code
if response.status_code != 200 or repo_response.status_code != 200:
    sys.exit(1)