#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Password Extractor Module
Extracts saved WiFi passwords from Windows
"""

import subprocess
import re
from typing import Optional, List, Dict
import os

class PasswordExtractor:
    def __init__(self):
        self.profiles = []
        
    def get_all_profiles(self) -> List[str]:
        """
        Get all saved WiFi profiles
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "profiles"],
                capture_output=True,
                text=True
            )
            
            profiles = []
            for line in result.stdout.split('\n'):
                if "All User Profile" in line:
                    match = re.search(r':\s*(.+)', line)
                    if match:
                        profiles.append(match.group(1).strip())
            
            return profiles
            
        except Exception as e:
            print(f"[!] Error getting profiles: {str(e)}")
            return []
    
    def get_password(self, ssid: str) -> Optional[str]:
        """
        Extract password for specific WiFi network
        """
        try:
            result = subprocess.run(
                ["netsh", "wlan", "show", "profile", f"name={ssid}", "key=clear"],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.split('\n'):
                if "Key Content" in line and ':' in line:
                    password = line.split(':', 1)[1].strip()
                    if password:
                        return password
            
            return None
            
        except Exception as e:
            print(f"[!] Error extracting password for {ssid}: {str(e)}")
            return None
    
    def get_current_password(self) -> Optional[str]:
        """
        Get password for currently connected WiFi network
        """
        try:
            # Get current connected SSID
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True
            )
            
            current_ssid = None
            for line in result.stdout.split('\n'):
                if "SSID" in line and ':' in line and "State" not in line:
                    match = re.search(r'SSID\s*:\s*([^\n]+)', line)
                    if match:
                        current_ssid = match.group(1).strip()
                        break
            
            if current_ssid:
                return self.get_password(current_ssid)
            
            return None
            
        except Exception as e:
            print(f"[!] Error getting current password: {str(e)}")
            return None
    
    def export_all_passwords(self) -> Dict[str, str]:
        """
        Export all saved WiFi passwords
        """
        passwords = {}
        profiles = self.get_all_profiles()
        
        for profile in profiles:
            password = self.get_password(profile)
            if password:
                passwords[profile] = password
        
        return passwords
    
    def export_to_file(self, filename: str) -> bool:
        """
        Export all passwords to file
        """
        try:
            passwords = self.export_all_passwords()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("WiFi Networks and Passwords\n")
                f.write("=" * 50 + "\n\n")
                
                for ssid, password in passwords.items():
                    f.write(f"SSID: {ssid}\n")
                    f.write(f"Password: {password}\n")
                    f.write("-" * 50 + "\n")
            
            return True
            
        except Exception as e:
            print(f"[!] Error exporting passwords: {str(e)}")
            return False
    
    def get_password_strength(self, password: str) -> Dict:
        """
        Analyze password strength
        """
        strength = {
            'length': len(password),
            'has_upper': any(c.isupper() for c in password),
            'has_lower': any(c.islower() for c in password),
            'has_digit': any(c.isdigit() for c in password),
            'has_special': any(not c.isalnum() for c in password),
            'score': 0
        }
        
        # Calculate strength score
        if len(password) >= 8:
            strength['score'] += 1
        if len(password) >= 12:
            strength['score'] += 1
        if strength['has_upper']:
            strength['score'] += 1
        if strength['has_lower']:
            strength['score'] += 1
        if strength['has_digit']:
            strength['score'] += 1
        if strength['has_special']:
            strength['score'] += 1
        
        strength['rating'] = self._get_strength_rating(strength['score'])
        
        return strength
    
    @staticmethod
    def _get_strength_rating(score: int) -> str:
        """
        Get strength rating based on score
        """
        if score <= 1:
            return "Very Weak"
        elif score <= 2:
            return "Weak"
        elif score <= 3:
            return "Fair"
        elif score <= 4:
            return "Good"
        elif score <= 5:
            return "Strong"
        else:
            return "Very Strong"
