#!/bin/bash

# SimpleBot setup script

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo "Checking Python version..."
if command_exists python3; then
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
  PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
  PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
  
  echo "Found Python $PYTHON_VERSION"
  
  if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "Error: Python 3.8 or higher is required. Found Python $PYTHON_VERSION"
    exit 1
  fi
else
  echo "Error: Python 3 not found. Please install Python 3.8 or higher."
  exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies with better error handling
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if pythorhead was installed correctly
if ! python3 -c "import pythorhead" &>/dev/null; then
  echo "Warning: pythorhead module not installed correctly. Trying alternative installation..."
  
  # Try installing the latest version without version constraint
  pip install pythorhead
  
  # Check again
  if ! python3 -c "import pythorhead" &>/dev/null; then
    echo "Error: Failed to install pythorhead. Please install it manually:"
    echo "  source venv/bin/activate"
    echo "  pip install pythorhead"
    echo ""
    echo "Then try running the bot again."
  else
    echo "Successfully installed pythorhead using alternative method."
  fi
fi

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