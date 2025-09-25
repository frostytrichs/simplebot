#!/bin/bash

# SimpleBot setup script

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit the .env file with your credentials."
fi

# Make main.py executable
chmod +x main.py

echo "Setup complete!"
echo "To run the bot:"
echo "  1. Edit .env with your credentials"
echo "  2. Edit config files in the config directory"
echo "  3. Run './main.py' or 'python main.py'"