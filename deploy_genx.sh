#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# Example of how to use the environment variables
echo "Deploying with Docker user: $DOCKER_USERNAME"
echo "Using Gemini API Key: $GEMINI_API_KEY"

# Your deployment logic here...