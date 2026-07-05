#!/bin/bash
# Install DocStruct on Cisco UCS / Linux server for team access
# Run as root: sudo bash deploy/install_on_server.sh
#
# After install, team opens: http://<SERVER-IP>:8501
# Demo login: demo / demo123

set -e

APP_DIR="/opt/docstruct"
APP_USER="docstruct"
APP_PORT=8501

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with sudo: sudo bash deploy/install_on_server.sh"
  exit 1
fi

echo "==> Installing system packages..."
if command -v apt-get &>/dev/null; then
  apt-get update -qq
  apt-get install -y python3 python3-pip python3-venv git
elif command -v yum &>/dev/null; then
  yum install -y python3 python3-pip git
elif command -v dnf &>/dev/null; then
  dnf install -y python3 python3-pip git
else
  echo "Install python3, pip, and venv manually, then re-run."
  exit 1
fi

echo "==> Creating app user..."
id "$APP_USER" &>/dev/null || useradd -r -m -d "$APP_DIR" -s /bin/bash "$APP_USER"

echo "==> Copying project to $APP_DIR..."
mkdir -p "$APP_DIR"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rsync -a --exclude venv --exclude data --exclude .git --exclude __pycache__ \
  "$SCRIPT_DIR/" "$APP_DIR/"

echo "==> Setting up Python virtual environment..."
sudo -u "$APP_USER" python3 -m venv "$APP_DIR/venv"
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install --upgrade pip -q
sudo -u "$APP_USER" "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" -q

echo "==> Creating data directory..."
mkdir -p "$APP_DIR/data"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

echo "==> Installing systemd service..."
cp "$APP_DIR/deploy/docstruct.service" /etc/systemd/system/docstruct.service
systemctl daemon-reload
systemctl enable docstruct
systemctl restart docstruct

echo "==> Opening firewall port $APP_PORT (if firewalld is active)..."
if systemctl is-active firewalld &>/dev/null; then
  firewall-cmd --permanent --add-port=${APP_PORT}/tcp
  firewall-cmd --reload
elif command -v ufw &>/dev/null && ufw status | grep -q active; then
  ufw allow ${APP_PORT}/tcp
fi

SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
echo ""
echo "============================================"
echo "  DocStruct is running!"
echo "  Team URL: http://${SERVER_IP:-YOUR-SERVER-IP}:${APP_PORT}"
echo "  Login:    demo / demo123"
echo "============================================"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status docstruct"
echo "  sudo systemctl restart docstruct"
echo "  sudo journalctl -u docstruct -f"