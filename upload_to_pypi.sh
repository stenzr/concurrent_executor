#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error occurred in step: $1"
    exit 1
}

echo "Starting build and upload process..."

# Remove previous build artifacts
echo "Removing previous build artifacts..."
rm -rf dist build *.egg-info || handle_error "Removing previous build artifacts"
echo "Previous build artifacts removed."

# Create source distribution and wheel
echo "Creating source distribution and wheel..."
python3 setup.py sdist bdist_wheel || handle_error "Creating source distribution and wheel"
echo "Source distribution and wheel created."

# Upload to PyPI using twine
echo "Uploading to PyPI..."
twine upload --repository pypi --verbose dist/* || handle_error "Uploading to PyPI"
echo "Upload to PyPI completed."

# Print finishing message
echo "Build and upload process finished."
