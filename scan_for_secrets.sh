#!/bin/bash

# This script scans the repository for secrets using TruffleHog.
# It is intended to be run manually before committing code.

echo "🐷 Running TruffleHog to scan for secrets..."

# The 'trufflehog filesystem' command scans the local file system.
# The '--fail' argument causes the script to exit with a non-zero status
# if any secrets are found, which is useful for CI/CD environments.
trufflehog filesystem . --fail

# Check the exit code of the trufflehog command
if [ $? -eq 0 ]; then
    echo "✅ No secrets found."
else
    echo "🚨 DANGER: Secrets were found in the repository. Please remove them before committing."
    exit 1
fi