#!/bin/bash

# Function to handle errors
handle_error() {
    echo "Error occurred in step: $1"
    exit 1
}

# Exit on any error
set -e

echo "Updating Release on Github..."

# Extract version from setup.py
echo "Extracting version from setup.py..."
VERSION=$(python setup.py --version) || handle_error "Failed to extract version from setup.py"
TAG_NAME="v${VERSION}"
RELEASE_NAME="Release ${TAG_NAME}"

echo "Extracted version: ${VERSION}"
echo "Tag name: ${TAG_NAME}"
echo "Release name: ${RELEASE_NAME}"

# Create a Git tag
echo "Creating Git tag..."
git tag -a "${TAG_NAME}" -m "Release ${TAG_NAME}" || handle_error "Failed to create Git tag"

# Push the tag to the remote repository
echo "Pushing Git tag to remote repository..."
git push origin "${TAG_NAME}" || handle_error "Failed to push Git tag to remote repository"

# Check if GitHub CLI is installed and install if necessary
if ! command -v gh &> /dev/null; then
  echo "GitHub CLI (gh) is not installed. Installing..."
  
  # Check the operating system
  OS=$(uname)
  if [[ "$OS" == "Linux" ]]; then
    sudo apt-get update || handle_error "Failed to update package list"
    sudo apt-get install -y gh || handle_error "Failed to install GitHub CLI"
  elif [[ "$OS" == "Darwin" ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
      echo "Homebrew is not installed. Installing..."
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || handle_error "Failed to install Homebrew"
    fi
    brew install gh || handle_error "Failed to install GitHub CLI with Homebrew"
  else
    handle_error "Unsupported operating system: $OS"
  fi
else
  echo "GitHub CLI (gh) is already installed."
fi

# Create a GitHub release
echo "Creating GitHub release..."
gh release create "${TAG_NAME}" --title "${RELEASE_NAME}" --notes "Published release ${TAG_NAME}." || handle_error "Failed to create GitHub release"

echo "GitHub release ${RELEASE_NAME} created successfully."
