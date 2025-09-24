# Security Audit: Hardcoded Secrets

This document summarizes the findings of a security audit that scanned the repository for hardcoded secrets.

## Critical Exposures

The following files contain multiple, high-priority secrets such as API keys and passwords that are exposed in plaintext. These must be removed immediately.

- **`deploy_genx.sh`**: Contains numerous hardcoded secrets, including:
  - `GEMINI_API_KEY`
  - `VANTAGE_ALPHAVANTAGE_API_KEY`
  - `NEWS_API_KEY`
  - `NEWSDATA_API_KEY`
  - `FINNHUB_API_KEY`
  - `GMAIL_APP_API_KEY`
  - `DOCKER_PASSWORD`
  - `GMAIL_PASSWORD`
  - `REDDIT_PASSWORD`
  - `FXCM_PASSWORD`
  - `REDDIT_CLIENT_SECRET`
  - `JWT_SECRET_KEY`
  - `TELEGRAM_BOT_TOKEN`

- **`deploy_genx_fixed.sh`**: A duplicate of `deploy_genx.sh` with the same hardcoded secrets.

## Other Exposures

The following files contain other hardcoded tokens, default passwords, or placeholder secrets that should be removed from the repository:

- **`quick_deploy_amp_gcs.sh`**: `AMP_TOKEN`, `GITHUB_TOKEN`
- **`setup-all-secrets.py`**: `CURSOR_CLI_API_KEY`
- **`google-drive-deploy.py`**: `CLIENT_SECRET_FILE`
- **`deploy/github-token-aws-deploy.sh`**: Default `GITHUB_TOKEN`
- **`deploy/github_aws_deploy.py`**: Default `GITHUB_TOKEN`
- **`update-github-profile.py`**: `GITHUB_TOKEN`
- **`deploy_heroku.sh`**: `HEROKU_TOKEN`
- **`aws/terraform/user_data.sh`**: `AMP_TOKEN`
- **`aws/amp-deploy.sh`**: `AMP_TOKEN`
- **`final_setup.sh`**, **`simple_setup.sh`**, **`direct_setup.sh`**, **`local_setup.sh`**, **`container_setup.sh`**: `MT5_PASSWORD`, `HEROKU_TOKEN`
- **`simple-migration.bat`**: `VULTR_SERVER_PASSWORD`
- **`DOCKER_DEPLOYMENT_GUIDE.md`**, **`DOCKER_DEPLOYMENT_SUMMARY.md`**: `DOCKER_PASSWORD`
- **`setup_github_token_aws.sh`**: Default `GITHUB_TOKEN`
- **`GITHUB_TOKEN_AWS_DEPLOYMENT.md`**: Default `GITHUB_TOKEN`
- **`auto_setup_github_secrets.sh`**: Default `AMP_TOKEN`
- **`GITHUB_SECRETS_GUIDE.md`**: Default `AMP_TOKEN`
- **`COMPLETE_GITHUB_SECRETS_SETUP.md`**: Default `AMP_TOKEN`
- **`deploy_amp_gcs.sh`**: `AMP_TOKEN`, `GITHUB_TOKEN`

## Plan of Action

The next steps will involve:
1.  Updating `.gitignore` to prevent future commits of sensitive files.
2.  Refactoring the application to load all secrets from environment variables.
3.  Removing all identified hardcoded secrets from the codebase.
4.  Creating a `.env.template` file to document required variables.
5.  Verifying the fix by running the application and tests.