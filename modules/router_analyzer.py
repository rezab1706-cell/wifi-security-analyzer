#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Router Analyzer Module
Analyzes router configuration and security settings
"""

import subprocess
import re
import socket
from typing import Dict, List, Optional
from urllib.request import urlopen, Request
import json

class RouterAnalyzer:
    def __init__(self, gateway: str = "192.168.1.1"):
        self.gateway = gateway
        self.config = {}
        
    def analyze(self) -> Dict:
        """
        Perform comprehensive router analysis
        """
        analysis = {
            'gateway': self.gateway,
            'reachable': self._is_gateway_reachable(),
            'firmware': self.get_firmware_info(),
            'services': self.get_open_services(),
            'dns': self.get_dns_config(),
            'dhcp': self.get_dhcp_config(),
            'security': self.get_security_config(),
            'interfaces': self.get_network_interfaces(),
        }
        return analysis
    
    def _is_gateway_reachable(self) -> bool:
        """
        Check if gateway is reachable
        """
        try:
            result = subprocess.run(
                ["ping", "-n", "1", self.gateway],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_firmware_info(self) -> Dict:
        """
        Get router firmware information
        """
        # This would need HTTP requests to router
        return {
            'status': 'Requires authentication',
            'method': 'HTTP GET /admin'
        }
    
    def get_open_services(self) -> List[Dict]:
        """
        Get list of open services on router
        """
        common_ports = [
            {'port': 80, 'service': 'HTTP', 'protocol': 'tcp'},
            {'port': 443, 'service': 'HTTPS', 'protocol': 'tcp'},
            {'port': 22, 'service': 'SSH', 'protocol': 'tcp'},
            {'port': 23, 'service': 'Telnet', 'protocol': 'tcp'},
            {'port': 53, 'service': 'DNS', 'protocol': 'udp'},
            {'port': 67, 'service': 'DHCP', 'protocol': 'udp'},
            {'port': 8080, 'service': 'HTTP Alt', 'protocol': 'tcp'},
        ]
        
        open_services = []
        for service in common_ports:
            if self._port_open(service['port']):
                open_services.append(service)
        
        return open_services
    
    def _port_open(self, port: int) -> bool:
        """
        Check if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.gateway, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_dns_config(self) -> Dict:
        """
        Get DNS configuration
        """
        try:
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True
            )
            
            dns_servers = []
            for line in result.stdout.split('\n'):
                if 'DNS Server' in line:
                    match = re.search(r'([\d.]+)', line)
                    if match:
                        dns_servers.append(match.group(1))
            
            return {'dns_servers': dns_servers}
        except Exception:
            return {'dns_servers': []}
    
    def get_dhcp_config(self) -> Dict:
        """
        Get DHCP configuration
        """
        try:
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True
            )
            
            dhcp_config = {}
            for line in result.stdout.split('\n'):
                if 'DHCP Enabled' in line:
                    dhcp_config['enabled'] = 'Yes' in line
                if 'DHCP Server' in line:
                    match = re.search(r'([\d.]+)', line)
                    if match:
                        dhcp_config['server'] = match.group(1)
            
            return dhcp_config
        except Exception:
            return {}
    
    def get_security_config(self) -> Dict:
        """
        Get security configuration
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "networks", "mode=Bssid"],
                capture_output=True,
                text=True
            )
            
            security = {
                'wpa2_enabled': 'WPA2' in result.stdout,
                'wpa3_enabled': 'WPA3' in result.stdout,
                'wep_enabled': 'WEP' in result.stdout,
                'open_networks': 'Open' in result.stdout,
            }
            
            return security
        except Exception:
            return {}
    
    def get_network_interfaces(self) -> List[Dict]:
        """
        Get network interfaces information
        """
        try:
            result = subprocess.run(
                ["ipconfig", "/all"],
                capture_output=True,
                text=True
            )
            
            interfaces = []
            current_interface = {}
            
            for line in result.stdout.split('\n'):
                if 'adapter' in line.lower():
                    if current_interface:
                        interfaces.append(current_interface)
                    current_interface = {'name': line.split(':')[0].strip()}
                elif 'IPv4 Address' in line:
                    match = re.search(r'([\d.]+)', line)
                    if match:
                        current_interface['ipv4'] = match.group(1)
                elif 'Physical Address' in line:
                    match = re.search(r'([0-9A-F-]+)', line)
                    if match:
                        current_interface['mac'] = match.group(1)
            
            if current_interface:
                interfaces.append(current_interface)
            
            return interfaces
        except Exception:
            return []
