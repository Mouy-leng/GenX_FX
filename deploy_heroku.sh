#!/bin/bash

# Heroku Deployment Script for GenX-FX Trading Platform
# This script sets up Heroku deployment with PostgreSQL database and SSH key configuration.
# It has been updated to remove hardcoded secrets for improved security.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Setting up Heroku deployment for GenX-FX Trading Platform${NC}"

# --- Pre-flight Check ---
# Check for the Heroku token as an environment variable
if [ -z "$HEROKU_TOKEN" ]; then
    echo -e "${RED}❌ Error: HEROKU_TOKEN environment variable is not set.${NC}"
    echo -e "${YELLOW}Please export your Heroku authentication token before running this script:${NC}"
    echo "  export HEROKU_TOKEN='your_heroku_auth_token'"
    exit 1
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo -e "${YELLOW}Installing Heroku CLI...${NC}"
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# --- SSH Key Setup ---
# Check if we have an SSH key, and generate one if it doesn't exist.
if [ ! -f ~/.ssh/id_rsa ]; then
    echo -e "${YELLOW}Generating SSH key for Heroku...${NC}"
    ssh-keygen -t rsa -b 4096 -C "heroku-deployment@genx-fx.com" -f ~/.ssh/id_rsa -N ""
    echo -e "${GREEN}✅ SSH key generated successfully.${NC}"
fi

# Add SSH key to the SSH agent to be used for authentication.
echo -e "${YELLOW}Adding SSH key to agent...${NC}"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# --- Heroku Application Setup ---
echo -e "${YELLOW}Logging into Heroku using the provided token...${NC}"
heroku auth:token <<< "$HEROKU_TOKEN"

# Create a unique Heroku app name using a timestamp.
APP_NAME="genx-fx-$(date +%s)"
echo -e "${YELLOW}Creating Heroku app: $APP_NAME${NC}"
heroku create $APP_NAME --json

# Add the PostgreSQL addon for the database.
echo -e "${YELLOW}Adding PostgreSQL database...${NC}"
heroku addons:create heroku-postgresql:mini --app $APP_NAME

echo -e "${YELLOW}Waiting for the database to be ready...${NC}"
sleep 10 # Wait for Heroku to provision the database.

# Set environment variables for the Heroku application.
echo -e "${YELLOW}Setting environment variables...${NC}"
heroku config:set ENVIRONMENT=production --app $APP_NAME
heroku config:set SECRET_KEY=$(openssl rand -hex 32) --app $APP_NAME
heroku config:set PYTHON_VERSION=3.11.7 --app $APP_NAME

# Get the database URL to confirm it's set up.
DATABASE_URL=$(heroku config:get DATABASE_URL --app $APP_NAME)
echo -e "${GREEN}Database URL has been configured.${NC}"

# Add the SSH key to the Heroku app for git push authentication.
echo -e "${YELLOW}Adding SSH key to Heroku...${NC}"
heroku keys:add ~/.ssh/id_rsa.pub --app $APP_NAME

# --- Deployment ---
echo -e "${YELLOW}Staging changes for deployment...${NC}"
git add .

echo -e "${YELLOW}Committing changes...${NC}"
git commit -m "Automated commit for Heroku deployment" || echo "No new changes to commit."

echo -e "${YELLOW}Adding Heroku git remote...${NC}"
heroku git:remote -a $APP_NAME

echo -e "${YELLOW}Deploying to Heroku...${NC}"
# Push the main branch to Heroku to trigger a build and deployment.
git push heroku main

# --- Post-Deployment Tasks ---
echo -e "${YELLOW}Setting up database schema...${NC}"
heroku run python setup_database.py --app $APP_NAME

echo -e "${YELLOW}Testing application...${NC}"
heroku run python -c "from api.main import app; print('✅ Application test successful')" --app $APP_NAME

echo -e "${GREEN}Opening application in browser...${NC}"
heroku open --app $APP_NAME

echo -e "${GREEN}✅ Heroku deployment complete!${NC}"
echo -e "App URL: https://$APP_NAME.herokuapp.com"

# --- Save Deployment Info ---
# Save deployment information to a file, excluding the sensitive token.
cat > heroku_deployment_info.txt << EOF
Heroku Deployment Information
============================
App Name: $APP_NAME
App URL: https://$APP_NAME.herokuapp.com
Database URL: [View in Heroku Dashboard or via 'heroku config:get DATABASE_URL']
Environment: production
Deployment Date: $(date)

Useful Commands:
- View logs: heroku logs --tail --app $APP_NAME
- Run commands: heroku run <command> --app $APP_NAME
- Open app: heroku open --app $APP_NAME
- Scale dynos: heroku ps:scale web=1 --app $APP_NAME
- Database console: heroku pg:psql --app $APP_NAME
EOF

echo -e "${GREEN}📝 Deployment information saved to heroku_deployment_info.txt${NC}"
echo -e "${BLUE}🔑 SSH key is ready for secure connections.${NC}"
echo -e "${BLUE}🗄️  PostgreSQL database is configured and ready.${NC}"