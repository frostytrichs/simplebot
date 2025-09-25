#!/bin/bash

# Script to fix pythorhead installation issues

echo "SimpleBot - Fix pythorhead installation"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Please run setup.sh first to create the virtual environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Try different installation methods for pythorhead
echo "Attempting to install pythorhead..."

# Method 1: Try latest version
echo "Method 1: Installing latest version..."
pip install --upgrade pythorhead

# Check if installation succeeded
if python3 -c "import pythorhead; print(f'Success! pythorhead version {pythorhead.__version__} installed')" 2>/dev/null; then
    echo "pythorhead installed successfully!"
    exit 0
fi

# Method 2: Try specific version
echo "Method 1 failed. Trying Method 2: Installing specific version..."
pip install pythorhead==0.34.0

# Check if installation succeeded
if python3 -c "import pythorhead; print(f'Success! pythorhead version {pythorhead.__version__} installed')" 2>/dev/null; then
    echo "pythorhead installed successfully!"
    exit 0
fi

# Method 3: Try with --no-cache-dir
echo "Method 2 failed. Trying Method 3: Installing with --no-cache-dir..."
pip install --no-cache-dir pythorhead

# Check if installation succeeded
if python3 -c "import pythorhead; print(f'Success! pythorhead version {pythorhead.__version__} installed')" 2>/dev/null; then
    echo "pythorhead installed successfully!"
    exit 0
fi

# If we get here, all methods failed
echo "Failed to install pythorhead after trying multiple methods."
echo ""
echo "Please try the following manual steps:"
echo "1. Make sure you have a compatible Python version (3.8 or higher)"
echo "2. Try installing with pip directly:"
echo "   source venv/bin/activate"
echo "   pip install pythorhead"
echo ""
echo "If the issue persists, please check TROUBLESHOOTING.md for more information."
exit 1