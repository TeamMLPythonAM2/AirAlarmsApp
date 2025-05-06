#!/bin/bash
set -e

git pull origin main
cd ui && npm install
cd app pip install -r requirements.txt
tsc -b && vite build
sudo systemctl restart airalarmsapp.service