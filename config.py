#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration File for WiFi Security Analyzer
"""

import os
from pathlib import Path

# Application Settings
APP_NAME = "WiFi Security Analyzer"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Reza"

# Windows Specific
WINDOWS_REQUIRED = True
ADMIN_REQUIRED = True

# Directories
BASE_DIR = Path(__file__).parent
MODULES_DIR = BASE_DIR / "modules"
UTILS_DIR = BASE_DIR / "utils"
WORDLISTS_DIR = BASE_DIR / "wordlists"
OUTPUT_DIR = BASE_DIR / "output"
HANDSHAKES_DIR = OUTPUT_DIR / "handshakes"
REPORTS_DIR = OUTPUT_DIR / "reports"

# Create directories if they don't exist
for directory in [OUTPUT_DIR, HANDSHAKES_DIR, REPORTS_DIR, WORDLISTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# WiFi Scanner Settings
WIFI_SCAN_TIMEOUT = 30
WIFI_SCAN_RETRIES = 3
WIFI_INTERFACE_INDEX = 0

# Vulnerability Scanner Settings
VULN_SCAN_TIMEOUT = 60
VULN_COMMON_VULNERABILITIES = [
    "Default Credentials",
    "Weak Encryption",
    "Open Network",
    "WPS Enabled",
    "Outdated Firmware",
    "Broadcast SSID",
]

# Handshake Capture Settings
HANDSHAKE_TIMEOUT = 300  # 5 minutes
HANDSHAKE_PACKET_COUNT = 4

# Brute Force Settings
BRUTE_FORCE_TIMEOUT = 600
BRUTE_FORCE_THREADS = 4
BRUTE_FORCE_CHUNK_SIZE = 1000
BRUTE_FORCE_DICTIONARY = WORDLISTS_DIR / "rockyou.txt"

# Common WiFi Passwords Wordlist
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "passw0rd", "shadow", "123123", "654321",
    "superman", "qazwsx", "michael", "football", "soccer",
    "admin", "password123", "12345678910", "1q2w3e4r", "qwerty123",
]

# Router Default Credentials
DEFAULT_ROUTER_CREDS = {
    "TP-Link": [("admin", "admin")],
    "D-Link": [("admin", "admin"), ("admin", "")],
    "Netgear": [("admin", "password")],
    "ASUS": [("admin", "admin")],
    "Linksys": [("admin", "admin")],
    "Cisco": [("admin", "cisco")],
}

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = OUTPUT_DIR / "analyzer.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

# Report Settings
REPORT_FORMAT = "pdf"  # or "html"
REPORT_INCLUDE_CHARTS = True
REPORT_INCLUDE_DETAILS = True

# Security Settings
WPA_ENCRYPTION_STRENGTH = 256
WPA2_ENCRYPTION_STRENGTH = 256
MIN_PASSWORD_LENGTH = 8
RECOMMENDED_PASSWORD_LENGTH = 12

# Network Settings
DEFAULT_GATEWAY_TIMEOUT = 5
NETWORK_INTERFACE_RETRY = 3
PING_PACKET_COUNT = 4

# Output Colors (for CLI)
COLORS = {
    "SUCCESS": "\033[92m",  # Green
    "ERROR": "\033[91m",    # Red
    "WARNING": "\033[93m",  # Yellow
    "INFO": "\033[94m",     # Blue
    "CRITICAL": "\033[95m", # Magenta
    "RESET": "\033[0m",
}
