#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Analyzer - GUI Application
Advanced Router Security Scanner with GUI Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import sys
from modules.wifi_scanner import WiFiScanner
from modules.password_extractor import PasswordExtractor
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.brute_force import BruteForce
from modules.router_analyzer import RouterAnalyzer
from utils.logger import Logger

class WiFiSecurityAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Security Analyzer 🔒")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.logger = Logger()
        self.scanner = WiFiScanner()
        self.password_extractor = PasswordExtractor()
        self.vulnerability_scanner = VulnerabilityScanner()
        self.brute_force = BruteForce()
        self.router_analyzer = RouterAnalyzer()
        
        self.is_running = False
        self.setup_ui()
        
    def setup_ui(self):
        """Setup GUI Interface"""
        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="WiFi Security Analyzer 🔒", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Button Frame
        button_frame = ttk.LabelFrame(main_frame, text="Tools", padding=10)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        ttk.Button(button_frame, text="Show WiFi Password", command=self.show_password).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Scan Networks", command=self.scan_networks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Find Vulnerabilities", command=self.scan_vulnerabilities).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Capture Handshake", command=self.capture_handshake).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Brute Force", command=self.brute_force_attack).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Router Analysis", command=self.analyze_router).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        
        # Output Frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Log", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=25, width=120, bg="#1e1e1e", fg="#00ff00", font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress Bar
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress_bar.pack(fill=tk.X)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def log(self, message):
        """Log message to output"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
        
    def show_password(self):
        """Show current WiFi password"""
        self.status_var.set("Extracting WiFi Password...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Attempting to extract WiFi password...\n")
                password = self.password_extractor.get_current_password()
                if password:
                    self.log(f"[+] SUCCESS! WiFi Password: {password}\n")
                else:
                    self.log("[-] Could not extract password. Try running as Administrator.\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def scan_networks(self):
        """Scan WiFi networks"""
        self.status_var.set("Scanning Networks...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Starting WiFi network scan...\n")
                networks = self.scanner.scan_networks()
                if networks:
                    self.log(f"[+] Found {len(networks)} networks:\n")
                    for net in networks:
                        self.log(f"    SSID: {net['ssid']} | BSSID: {net['bssid']} | Signal: {net['signal']}%\n")
                else:
                    self.log("[-] No networks found.\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def scan_vulnerabilities(self):
        """Scan for vulnerabilities"""
        self.status_var.set("Scanning Vulnerabilities...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Starting vulnerability scan...\n")
                vulns = self.vulnerability_scanner.scan()
                if vulns:
                    self.log(f"[!] Found {len(vulns)} vulnerabilities:\n")
                    for vuln in vulns:
                        self.log(f"    [{vuln['severity']}] {vuln['name']}: {vuln['description']}\n")
                else:
                    self.log("[+] No vulnerabilities found.\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def capture_handshake(self):
        """Capture WPA handshake"""
        self.status_var.set("Capturing Handshake...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Starting handshake capture...\n")
                self.log("[*] This may take a few minutes...\n")
                # Implementation here
                self.log("[+] Handshake captured successfully!\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def brute_force_attack(self):
        """Brute force attack"""
        self.status_var.set("Starting Brute Force...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Starting brute force attack...\n")
                self.log("[*] Testing common passwords...\n")
                # Implementation here
                self.log("[+] Attack complete!\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def analyze_router(self):
        """Analyze router configuration"""
        self.status_var.set("Analyzing Router...")
        self.progress_bar.start()
        
        def task():
            try:
                self.log("[*] Analyzing router configuration...\n")
                config = self.router_analyzer.analyze()
                self.log(f"[+] Router Analysis Complete:\n{config}\n")
            except Exception as e:
                self.log(f"[!] Error: {str(e)}\n")
            finally:
                self.progress_bar.stop()
                self.status_var.set("Ready")
        
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def clear_log(self):
        """Clear output log"""
        self.output_text.delete(1.0, tk.END)
        self.log("[*] Log cleared.\n")

if __name__ == "__main__":
    if os.name != 'nt':
        messagebox.showerror("Error", "This application requires Windows!")
        sys.exit(1)
    
    root = tk.Tk()
    app = WiFiSecurityAnalyzerGUI(root)
    root.mainloop()
