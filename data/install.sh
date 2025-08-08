#!/bin/bash

set -e

echo
echo "Thank you for installing the Linux Server Dashboard!"
echo "This script will install dependencies and set everything up."
echo
echo "Updating package lists..."
sudo apt-get update

echo "Installing dependencies..."
sudo apt-get install -y python3 python3-pip python3-venv git

echo "Cloning the repository..."
if [ ! -d "/opt/server-dashboard" ]; then
  sudo git clone https://github.com/Laith-Al/Linux-Server-Dashbosard.git /opt/server-dashboard
else
  echo "Repository already exists. Updating To Latest Version!"
  cd /opt/server-dashboard && sudo git pull
fi

echo "Setting up Python virtual environment..."
cd /opt/server-dashboard
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating systemd service..."
sudo tee /etc/systemd/system/server-dashboard.service > /dev/null <<EOF
[Unit]
Description=Server Dashboard
After=network.target

[Service]
User=root
WorkingDirectory=/opt/server-dashboard
ExecStart=/opt/server-dashboard/venv/bin/python /opt/server-dashboard/server.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling and starting the dashboard service..."
sudo systemctl daemon-reload
sudo systemctl enable server-dashboard
sudo systemctl start server-dashboard

echo
echo "Installation complete!"
echo "Visit http://<your-device-ip>:49200 in your browser."
echo "Thank you for using Linux Server Dashboard!"
