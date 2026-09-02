#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Scanner Module
Scans for available WiFi networks and their details
"""

import subprocess
import re
import json
from typing import List, Dict
import wmi
import socket
import struct
from config import WiFi_SCAN_TIMEOUT, WiFi_SCAN_RETRIES

class WiFiScanner:
    def __init__(self):
        self.timeout = WiFi_SCAN_TIMEOUT
        self.retries = WiFi_SCAN_RETRIES
        
    def scan_networks(self) -> List[Dict]:
        """
        Scan for available WiFi networks
        Returns list of networks with SSID, BSSID, Signal strength, Security
        """
        networks = []
        
        try:
            # Windows netsh command to get WiFi networks
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            output = result.stdout
            current_ssid = None
            current_network = {}
            
            for line in output.split('\n'):
                # Parse SSID
                if 'SSID' in line and ':' in line:
                    match = re.search(r'SSID\s*:\s*(.+)', line)
                    if match:
                        current_ssid = match.group(1).strip()
                        current_network = {
                            'ssid': current_ssid,
                            'bssid': '',
                            'signal': 0,
                            'security': '',
                            'encryption': ''
                        }
                
                # Parse BSSID
                if 'BSSID' in line and ':' in line:
                    match = re.search(r':\s*([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})', line)
                    if match:
                        current_network['bssid'] = match.group(1)
                
                # Parse Signal Strength
                if 'Signal' in line and '%' in line:
                    match = re.search(r'(\d+)%', line)
                    if match:
                        current_network['signal'] = int(match.group(1))
                
                # Parse Security Type
                if 'Authentication' in line:
                    match = re.search(r':\s*(.+)', line)
                    if match:
                        current_network['security'] = match.group(1).strip()
                
                # Parse Encryption
                if 'Encryption' in line:
                    match = re.search(r':\s*(.+)', line)
                    if match:
                        current_network['encryption'] = match.group(1).strip()
                        if current_network not in networks and current_network.get('ssid'):
                            networks.append(current_network.copy())
            
            return networks
            
        except Exception as e:
            print(f"[!] Error scanning networks: {str(e)}")
            return []
    
    def get_interface_info(self) -> Dict:
        """
        Get current WiFi interface information
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            return info
            
        except Exception as e:
            print(f"[!] Error getting interface info: {str(e)}")
            return {}
    
    def get_connected_network(self) -> Dict:
        """
        Get information about currently connected WiFi network
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            network = {}
            state = None
            
            for line in result.stdout.split('\n'):
                if 'State' in line and ':' in line:
                    state = line.split(':')[1].strip()
                if 'SSID' in line and ':' in line:
                    network['ssid'] = line.split(':', 1)[1].strip()
                if 'Signal' in line and '%' in line:
                    match = re.search(r'(\d+)%', line)
                    if match:
                        network['signal'] = int(match.group(1))
            
            network['state'] = state
            return network
            
        except Exception as e:
            print(f"[!] Error getting connected network: {str(e)}")
            return {}
    
    def scan_network_security(self, bssid: str) -> Dict:
        """
        Scan security details of specific network
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            security_info = {}
            in_target = False
            
            for line in result.stdout.split('\n'):
                if bssid in line:
                    in_target = True
                elif in_target:
                    if 'BSSID' in line or 'SSID' in line:
                        in_target = False
                    else:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            security_info[key.strip()] = value.strip()
            
            return security_info
            
        except Exception as e:
            print(f"[!] Error scanning network security: {str(e)}")
            return {}
