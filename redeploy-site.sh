#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting site redeployment for PE-portfolio..."

# 1. Kill all existing tmux sessions safely
echo "Killing existing tmux sessions..."
tmux kill-server || true

# 2. Navigate to your project directory
PROJECT_DIR="$HOME/PE-portfolio-SV-KG"
echo "Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# 3. Fetch latest changes and hard reset to match GitHub's main branch
echo "Fetching latest changes from GitHub..."
git fetch --all
git reset origin/main --hard

# 4. Activate virtual environment and install/update dependencies
echo "Activating virtual environment and installing dependencies..."
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# 5. Start a new detached tmux session named flask-app and launch Flask
echo "Starting Flask server inside a new tmux session..."
tmux new-session -d -s flask-app

# Send commands to the tmux session
tmux send-keys -t flask-app "source python3-virtualenv/bin/activate" C-m
tmux send-keys -t flask-app "flask run --host=0.0.0.0" C-m

echo "Redeployment complete! Your site is updating."
