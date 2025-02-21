#!/usr/bin/env bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Install Google Chrome
echo "Installing Google Chrome..."
apt-get update && apt-get install -y wget unzip curl gnupg
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Get the installed Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+' | head -n1)
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d '.' -f 1)

# Install matching ChromeDriver
echo "Installing ChromeDriver for Chrome version $CHROME_VERSION..."
wget -N https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip || wget -N https://chromedriver.storage.googleapis.com/${CHROME_MAJOR_VERSION}.0.0/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# Verify installations
echo "Verifying installations..."
which google-chrome
google-chrome --version
which chromedriver
chromedriver --version

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build process completed successfully."
