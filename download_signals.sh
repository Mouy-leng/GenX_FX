#!/bin/bash

# This script downloads live trading signals and saves them to the specified MT4 data folder.

# --- Configuration ---
API_URL="http://127.0.0.1:8000/api/signals"
DEFAULT_FILENAME="signals.csv"

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $0 <mt4_data_path>"
    echo "  <mt4_data_path>: The absolute path to your MT4 'Files' directory (e.g., '/path/to/your/mt4/MQL4/Files')."
    exit 1
}

# --- Main Script ---

# Check if the MT4 data path is provided
if [ -z "$1" ]; then
    echo "Error: MT4 data path not provided."
    usage
fi

MT4_DATA_PATH="$1"
OUTPUT_FILE="$MT4_DATA_PATH/$DEFAULT_FILENAME"

# Check if the target directory exists
if [ ! -d "$MT4_DATA_PATH" ]; then
    echo "Error: The directory '$MT4_DATA_PATH' does not exist."
    echo "Please ensure you provide the correct path to your MT4 'Files' directory."
    exit 1
fi

# Download the signals using curl
echo "Downloading signals from $API_URL..."
curl -s -o "$OUTPUT_FILE" "$API_URL"

# Check if curl was successful
if [ $? -eq 0 ]; then
    echo "Signals successfully downloaded to $OUTPUT_FILE"
    echo "---"
    echo "Latest signals:"
    cat "$OUTPUT_FILE"
else
    echo "Error: Failed to download signals. Please check that the API server is running."
    exit 1
fi