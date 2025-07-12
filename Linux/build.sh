#!/bin/bash

echo "Building AI Image Generator..."
echo

# Activate the Python virtual environment
echo "Activating Python virtual environment..."

# Try different common virtual environment locations
if [ -d "image-generator" ]; then
    source image-generator/bin/activate
    echo "Activated virtual environment from ./image-generator/"
elif [ -d "venv" ]; then
    source venv/bin/activate
    echo "Activated virtual environment from ./venv/"
elif [ -d "env" ]; then
    source env/bin/activate
    echo "Activated virtual environment from ./env/"
elif [ -d "../image-generator" ]; then
    source ../image-generator/bin/activate
    echo "Activated virtual environment from ../image-generator/"
else
    echo "Error: Could not find Python virtual environment"
    echo "Please make sure your virtual environment is in one of these locations:"
    echo "  - ./image-generator/"
    echo "  - ./venv/"
    echo "  - ./env/"
    echo "  - ../image-generator/"
    echo ""
    echo "Or modify this script to point to your virtual environment location"
    exit 1
fi

# Check if environment activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate Python virtual environment"
    echo "Make sure the environment exists and is properly configured"
    exit 1
fi

echo "Virtual environment activated: $VIRTUAL_ENV"

# Install PyInstaller if not already installed
echo "Installing PyInstaller..."
pip install pyinstaller

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist

# Build the executable using the spec file
echo "Building executable..."
pyinstaller --clean app.spec

# Check if build was successful
if [ -f "dist/AI_Image_Generator" ]; then
    echo
    echo "====================================="
    echo "Build completed successfully!"
    echo "Executable created: dist/AI_Image_Generator"
    echo "====================================="
    echo
    echo "To run the application:"
    echo "./dist/AI_Image_Generator"
    echo
else
    echo
    echo "====================================="
    echo "Build failed! Check the output above for errors."
    echo "====================================="
    echo
    exit 1
fi