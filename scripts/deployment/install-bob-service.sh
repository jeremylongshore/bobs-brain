#!/bin/bash
# Install Bob Ferrari as a systemd service for 24/7 operation

echo "🏎️ Installing Bob Ferrari Service..."

# Create logs directory
mkdir -p /home/jeremylongshore/bobs-brain/logs

# Copy service file
sudo cp bob-ferrari.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable bob-ferrari.service

# Start the service
sudo systemctl start bob-ferrari.service

# Check status
sudo systemctl status bob-ferrari.service

echo "✅ Bob Ferrari installed as systemd service!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status bob-ferrari   # Check status"
echo "  sudo systemctl restart bob-ferrari  # Restart service"
echo "  sudo systemctl stop bob-ferrari     # Stop service"
echo "  sudo journalctl -u bob-ferrari -f   # View logs"
echo "  tail -f ~/bobs-brain/logs/bob-ferrari.log  # View application logs"