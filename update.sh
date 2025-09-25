#!/bin/bash

# SimpleBot update script

# Check if the virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Pull latest changes from git
echo "Pulling latest changes from git..."
git pull

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Update dependencies
echo "Updating dependencies..."
pip install -r requirements.txt

echo "Update complete!"
echo "You may need to restart the bot for changes to take effect."