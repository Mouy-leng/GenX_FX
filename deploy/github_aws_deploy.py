#!/usr/bin/env python3
"""
GitHub Token AWS Deployment Script
Uses GitHub API with token authentication for AWS deployment.
This script has been updated to securely handle the GitHub token.
"""

import os
import sys
import json
import time
import argparse
import subprocess
import requests
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import docker
from docker.errors import DockerException

# --- Configuration ---
# The GitHub token MUST be loaded from an environment variable for security.
# Before running, set the token in your shell:
# export GITHUB_TOKEN='your_personal_access_token_here'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Default values
DEFAULT_ENVIRONMENT = 'production'
DEFAULT_AWS_REGION = 'us-east-1'
DEFAULT_BRANCH = 'main'

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class GitHubAWSDployer:
    """Main deployment class for GitHub token-based AWS deployment"""

    def __init__(self, environment: str, region: str, branch: str, token: str):
        self.environment = environment
        self.region = region
        self.branch = branch
        self.token = token
        self.github_headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.deployment_id = None
        self.deployment_url = None

        # Initialize AWS and Docker clients
        self.aws_session = None
        self.docker_client = None
        self.ecr_client = None

    def print_status(self, message: str):
        """Print status message with blue color"""
        print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

    def print_success(self, message: str):
        """Print success message with green color"""
        print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

    def print_warning(self, message: str):
        """Print warning message with yellow color"""
        print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

    def print_error(self, message: str):
        """Print error message with red color"""
        print(f"{Colors.RED}[ERROR]{Colors.NC} {message}", file=sys.stderr)

    def check_github_token(self) -> bool:
        """Check if GitHub token is valid"""
        try:
            response = requests.get('https://api.github.com/user', headers=self.github_headers)
            response.raise_for_status()
            user_data = response.json()
            self.print_success(f"GitHub authentication successful for user: {user_data['login']}")
            return True
        except requests.exceptions.RequestException as e:
            self.print_error(f"GitHub authentication failed: {e}")
            if e.response is not None:
                self.print_error(f"Response: {e.response.text}")
            return False

    def check_aws_credentials(self) -> bool:
        """Check if AWS credentials are configured"""
        try:
            self.aws_session = boto3.Session(region_name=self.region)
            sts_client = self.aws_session.client('sts')
            identity = sts_client.get_caller_identity()
            self.print_success(f"AWS credentials configured for account: {identity['Account']}")
            return True
        except NoCredentialsError:
            self.print_error("AWS credentials not found. Please configure them (e.g., via `aws configure` or environment variables).")
            return False
        except Exception as e:
            self.print_error(f"Failed to check AWS credentials: {e}")
            return False

    def setup_aws_from_github_secrets(self) -> bool:
        """Placeholder for setting up AWS creds from GitHub secrets."""
        self.print_warning("GitHub API does not allow direct reading of secrets for security reasons.")
        self.print_status("Please ensure AWS credentials are set as environment variables:")
        self.print_status("  export AWS_ACCESS_KEY_ID='your_access_key'")
        self.print_status("  export AWS_SECRET_ACCESS_KEY='your_secret_key'")
        self.print_status("  export AWS_DEFAULT_REGION='us-east-1'")
        return self.check_aws_credentials()

    def _get_repo_owner(self) -> str:
        """Get repository owner from git remote"""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                  capture_output=True, text=True, check=True)
            remote_url = result.stdout.strip()
            if 'github.com' in remote_url:
                parts = remote_url.split('github.com/')[-1].split('/')
                return parts[0]
            return 'unknown'
        except Exception:
            return 'unknown'

    def _get_repo_name(self) -> str:
        """Get repository name from git remote"""
        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                  capture_output=True, text=True, check=True)
            remote_url = result.stdout.strip()
            if 'github.com' in remote_url:
                parts = remote_url.split('github.com/')[-1].split('/')
                return parts[1].replace('.git', '')
            return 'unknown'
        except Exception:
            return 'unknown'

    def create_github_deployment(self) -> Optional[str]:
        """Create a GitHub deployment"""
        try:
            repo_owner = self._get_repo_owner()
            repo_name = self._get_repo_name()

            result = subprocess.run(['git', 'rev-parse', 'HEAD'],
                                  capture_output=True, text=True, check=True)
            commit_sha = result.stdout.strip()

            deployment_data = {
                'ref': commit_sha,
                'environment': self.environment,
                'description': f'Deployment to AWS {self.environment}',
                'auto_merge': False,
                'required_contexts': []
            }

            url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/deployments'
            response = requests.post(url, headers=self.github_headers, json=deployment_data)
            response.raise_for_status()

            deployment = response.json()
            self.deployment_id = str(deployment['id'])
            self.print_success(f"Created GitHub deployment with ID: {self.deployment_id}")
            return self.deployment_id

        except Exception as e:
            self.print_error(f"Failed to create GitHub deployment: {e}")
            return None

    def update_deployment_status(self, state: str, description: str, url: str = None) -> bool:
        """Update GitHub deployment status"""
        if not self.deployment_id:
            self.print_warning("No deployment ID available, cannot update status.")
            return False

        try:
            repo_owner = self._get_repo_owner()
            repo_name = self._get_repo_name()

            status_data = {'state': state, 'description': description}
            if url:
                status_data['environment_url'] = url

            status_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/deployments/{self.deployment_id}/statuses'
            response = requests.post(status_url, headers=self.github_headers, json=status_data)
            response.raise_for_status()

            self.print_success(f"Updated deployment status to: {state}")
            return True

        except Exception as e:
            self.print_error(f"Failed to update deployment status: {e}")
            return False

    def build_and_push_docker_images(self) -> bool:
        """Build and push Docker images to ECR"""
        try:
            self.docker_client = docker.from_env()
            sts_client = self.aws_session.client('sts')
            account_id = sts_client.get_caller_identity()['Account']
            ecr_registry = f"{account_id}.dkr.ecr.{self.region}.amazonaws.com"
            self.ecr_client = self.aws_session.client('ecr')

            auth_response = self.ecr_client.get_authorization_token()
            auth_data = auth_response['authorizationData'][0]
            ecr_token = auth_data['authorizationToken']

            self.docker_client.login(username='AWS', password=ecr_token, registry=ecr_registry)

            image_tag = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                                     capture_output=True, text=True, check=True).stdout.strip()

            self.print_status("Building main API image...")
            image, _ = self.docker_client.images.build(path='.', tag=f'{ecr_registry}/genx-api:{image_tag}')
            image.tag(f'{ecr_registry}/genx-api', 'latest')

            self.docker_client.images.push(f'{ecr_registry}/genx-api:{image_tag}')
            self.docker_client.images.push(f'{ecr_registry}/genx-api:latest')

            self.print_success("Docker images built and pushed successfully.")
            return True

        except (DockerException, ClientError, Exception) as e:
            self.print_error(f"Failed to build and push Docker images: {e}")
            return False

    def deploy_to_aws(self) -> bool:
        """Deploy to AWS using an existing deployment script."""
        try:
            self.print_status(f"Deploying to AWS {self.environment} environment...")
            script_path = 'deploy/aws-deploy.sh'
            if not os.path.exists(script_path):
                self.print_error(f"AWS deployment script not found at {script_path}")
                return False

            os.chmod(script_path, 0o755)
            result = subprocess.run([script_path, '--region', self.region, '--environment', self.environment],
                                  capture_output=True, text=True)

            if result.returncode == 0:
                self.print_success(f"AWS deployment script executed successfully:\n{result.stdout}")
                return True
            else:
                self.print_error(f"AWS deployment failed:\n{result.stderr}")
                return False

        except Exception as e:
            self.print_error(f"Failed to run AWS deployment script: {e}")
            return False

    def get_deployment_url(self) -> Optional[str]:
        """Get the deployment URL from CloudFormation outputs."""
        try:
            stack_name = f"{self.environment}-genx-trading-platform"
            cloudformation = self.aws_session.client('cloudformation')
            response = cloudformation.describe_stacks(StackName=stack_name)

            for output in response['Stacks'][0]['Outputs']:
                if output['OutputKey'] == 'LoadBalancerDNS':
                    self.deployment_url = f"http://{output['OutputValue']}"
                    self.print_success(f"Application URL: {self.deployment_url}")
                    return self.deployment_url
            return None
        except Exception as e:
            self.print_error(f"Failed to get deployment URL: {e}")
            return None

    def health_check(self, url: str, max_attempts: int = 30) -> bool:
        """Perform a health check on the deployed application."""
        self.print_status(f"Performing health check on {url}...")
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{url}/health", timeout=10)
                if response.ok:
                    self.print_success("Health check passed!")
                    return True
            except requests.RequestException:
                pass
            time.sleep(10)
        self.print_error("Health check failed.")
        return False

    def deploy(self) -> bool:
        """Main deployment method"""
        self.print_status("Starting GitHub Token AWS Deployment")

        if not self.check_github_token() or not self.check_aws_credentials():
            return False

        if not self.create_github_deployment():
            return False

        self.update_deployment_status("in_progress", "Starting deployment to AWS")

        if not self.build_and_push_docker_images() or not self.deploy_to_aws():
            self.update_deployment_status("failure", "Deployment to AWS failed")
            return False

        deployment_url = self.get_deployment_url()
        if deployment_url and self.health_check(deployment_url):
            self.update_deployment_status("success", "Deployment successful and healthy", deployment_url)
        else:
            self.update_deployment_status("failure", "Health check failed", deployment_url)
            return False

        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='GitHub Token AWS Deployment Script')
    parser.add_argument('-e', '--environment', default=DEFAULT_ENVIRONMENT, help='Environment to deploy to')
    parser.add_argument('-r', '--region', default=DEFAULT_AWS_REGION, help='AWS region')
    parser.add_argument('-b', '--branch', default=DEFAULT_BRANCH, help='Git branch to deploy')
    parser.add_argument('-t', '--token', default=GITHUB_TOKEN, help='GitHub personal access token')

    args = parser.parse_args()

    if not args.token:
        print(f"{Colors.RED}[ERROR]{Colors.NC} GitHub token not provided. Set GITHUB_TOKEN or use --token.", file=sys.stderr)
        sys.exit(1)

    deployer = GitHubAWSDployer(args.environment, args.region, args.branch, args.token)
    sys.exit(0 if deployer.deploy() else 1)

if __name__ == '__main__':
    main()