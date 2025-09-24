#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Your deployment logic here...
echo "Deploying with AMP Token: $AMP_TOKEN"
echo "Deploying with GitHub Token: $GITHUB_TOKEN"