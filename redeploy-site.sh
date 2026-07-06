#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting site redeployment for PE-portfolio..."

# 1. Navigate to your project directory
PROJECT_DIR="/root/PE-portfolio-SV-KG"
echo "Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# 2. Fetch latest changes and hard reset to match GitHub's main branch
echo "Fetching latest changes from GitHub..."
git fetch --all
git reset origin/main --hard

# 3. Activate virtual environment and install/update dependencies
echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# 4. Restart the systemd service
echo "Restarting myportfolio systemd service..."
sudo systemctl restart myportfolio

echo "Redeployment complete! Your site is updating via systemd."
