#!/bin/bash

echo "Starting build and upload process..."

# Remove previous build artifacts
echo "Removing previous build artifacts..."
rm -rf dist build *.egg-info
echo "Previous build artifacts removed."

# Create source distribution and wheel
echo "Creating source distribution and wheel..."
python3.12 setup.py sdist bdist_wheel
echo "Source distribution and wheel created."

# Upload to PyPI using twine
echo "Uploading to PyPI..."
twine upload --repository pypi --verbose dist/*


# Print finishing message
echo "Build and upload process finished."

