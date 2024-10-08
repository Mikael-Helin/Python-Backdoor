#!/bin/bash

# If user is not root, exit
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Test if python3 is installed
if ! [ -x "$(command -v python3)" ]; then
  echo 'Error: python3 is not installed.' >&2
  exit 1
fi

# Test if pip3 is installed
if ! [ -x "$(command -v pip3)" ]; then
  echo 'Error: pip3 is not installed.' >&2
  exit 1
fi

# Test if python3-venv is installed
if ! python3 -m venv --help > /dev/null 2>&1; then
  echo 'Error: python3-venv is not installed.' >&2
  exit 1
fi

# Create dirs
mkdir -p /opt/backdoor/bin
mkdir -p /opt/backdoor/config
mkdir -p /opt/backdoor/logs
mkdir -p /opt/backdoor/lib
mkdir -p /opt/backdoor/tmp

# Copy files
cp -r backdoor /usr/local/bin
chown root:root /usr/local/bin/backdoor
chmod +x /usr/local/bin/backdoor

cp backdoor.py /opt/backdoor/bin/backdoor.py
cp template.env /opt/backdoor/config/.env
chown root:root /opt/backdoor/config/.env
cp requirements.txt /opt/backdoor/lib/requirements.txt

# Install dependencies
if [ ! -d "/opt/backdoor/lib/venv" ]; then
  python3 -m venv /opt/backdoor/lib/venv
fi
source /opt/backdoor/lib/venv/bin/activate
pip3 install -r /opt/backdoor/lib/requirements.txt

echo "Installation completed successfully."
echo "Please edit /opt/backdoor/config/.env file and run backdoor command to start the server."
