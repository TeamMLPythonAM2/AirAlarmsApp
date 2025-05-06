#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "=== Starting CI/CD Pipeline ==="

# Step 1: Pull latest changes
echo "--- Pulling latest changes from Git ---"
git pull origin main

# Step 2: Install dependencies
echo "--- Installing dependencies ---"
cd ui && npm install
cd app pip install -r requirements.txt
# For Node.js
# npm install
# For Python
# pip install -r requirements.txt

# Step 3: Run tests
echo "--- Running tests ---"
# Node.js: npm test
# Python: pytest
# Java: ./gradlew test

# Step 4: Build the project
echo "--- Building project ---"
tsc -b && vite build
# Node.js: npm run build
# Java: ./gradlew build

# Step 5: Deploy
echo "--- Deploying application ---"
# Example: Copy build files to server or restart service
# rsync -avz ./build/ user@yourserver:/var/www/yourapp
# ssh user@yourserver 'sudo systemctl restart yourapp'
sudo systemctl restart airalarmsapp.service

echo "=== CI/CD Pipeline Complete ==="
