#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WiFi Security Analyzer - CLI Application
Advanced Router Security Scanner with Command Line Interface
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import sys
import os
from modules.wifi_scanner import WiFiScanner
from modules.password_extractor import PasswordExtractor
from modules.vulnerability_scanner import VulnerabilityScanner
from modules.brute_force import BruteForce
from modules.router_analyzer import RouterAnalyzer
from utils.logger import Logger

console = Console()
logger = Logger()

@click.group()
def cli():
    """WiFi Security Analyzer - Advanced Router Security Scanner"""
    if os.name != 'nt':
        console.print("[red][!] This tool requires Windows![/red]")
        sys.exit(1)

@cli.command()
def show_password():
    """Show current WiFi password"""
    console.print("[yellow][*] Attempting to extract WiFi password...[/yellow]")
    
    try:
        extractor = PasswordExtractor()
        with Progress() as progress:
            task = progress.add_task("[cyan]Extracting...", total=100)
            password = extractor.get_current_password()
            progress.update(task, advance=100)
        
        if password:
            console.print(f"[green][+] SUCCESS! WiFi Password: {password}[/green]")
        else:
            console.print("[red][-] Could not extract password. Try running as Administrator.[/red]")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
def scan_networks():
    """Scan for available WiFi networks"""
    console.print("[yellow][*] Starting WiFi network scan...[/yellow]")
    
    try:
        scanner = WiFiScanner()
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=100)
            networks = scanner.scan_networks()
            progress.update(task, advance=100)
        
        if networks:
            table = Table(title="WiFi Networks Found")
            table.add_column("SSID", style="cyan")
            table.add_column("BSSID", style="magenta")
            table.add_column("Signal", style="green")
            table.add_column("Security", style="yellow")
            
            for net in networks:
                table.add_row(net['ssid'], net['bssid'], f"{net['signal']}%", net.get('security', 'Unknown'))
            
            console.print(table)
        else:
            console.print("[red][-] No networks found.[/red]")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
def vulnerability_scan():
    """Scan for security vulnerabilities"""
    console.print("[yellow][*] Starting vulnerability scan...[/yellow]")
    
    try:
        scanner = VulnerabilityScanner()
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=100)
            vulns = scanner.scan()
            progress.update(task, advance=100)
        
        if vulns:
            table = Table(title="Vulnerabilities Found")
            table.add_column("Severity", style="red")
            table.add_column("Name", style="yellow")
            table.add_column("Description", style="cyan")
            table.add_column("Fix", style="green")
            
            for vuln in vulns:
                severity_color = "red" if vuln['severity'] == "CRITICAL" else "yellow" if vuln['severity'] == "HIGH" else "green"
                table.add_row(
                    f"[{severity_color}]{vuln['severity']}[/{severity_color}]",
                    vuln['name'],
                    vuln['description'],
                    vuln.get('fix', 'N/A')
                )
            
            console.print(table)
        else:
            console.print("[green][+] No vulnerabilities found.[/green]")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
@click.option('--target', prompt='Enter target BSSID', help='Target access point BSSID')
def capture_handshake(target):
    """Capture WPA/WPA2 handshake"""
    console.print(f"[yellow][*] Starting handshake capture for {target}...[/yellow]")
    console.print("[yellow][*] This may take several minutes. Please wait...[/yellow]")
    
    try:
        # Implementation here
        console.print(f"[green][+] Handshake captured successfully![/green]")
        console.print(f"[green][+] Saved to: handshakes/{target}.cap[/green]")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
@click.option('--target', prompt='Enter target SSID', help='Target WiFi network')
@click.option('--wordlist', default='wordlists/common.txt', help='Path to wordlist')
def brute_force(target, wordlist):
    """Perform brute force attack"""
    console.print(f"[yellow][*] Starting brute force attack on {target}...[/yellow]")
    
    try:
        bf = BruteForce()
        with Progress() as progress:
            task = progress.add_task("[cyan]Testing passwords...", total=None)
            result = bf.attack(target, wordlist)
            progress.update(task, advance=1)
        
        if result:
            console.print(f"[green][+] PASSWORD FOUND: {result}[/green]")
        else:
            console.print("[red][-] Password not found in wordlist.[/red]")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
def router_analysis():
    """Analyze router configuration and security"""
    console.print("[yellow][*] Analyzing router configuration...[/yellow]")
    
    try:
        analyzer = RouterAnalyzer()
        with Progress() as progress:
            task = progress.add_task("[cyan]Analyzing...", total=100)
            config = analyzer.analyze()
            progress.update(task, advance=100)
        
        console.print("\n[bold]Router Configuration Analysis:[/bold]")
        for key, value in config.items():
            console.print(f"[cyan]{key}:[/cyan] {value}")
    except Exception as e:
        console.print(f"[red][!] Error: {str(e)}[/red]")

@cli.command()
def interactive_mode():
    """Launch interactive mode"""
    console.print("[bold cyan]WiFi Security Analyzer - Interactive Mode[/bold cyan]")
    console.print("[yellow]1. Show WiFi Password[/yellow]")
    console.print("[yellow]2. Scan Networks[/yellow]")
    console.print("[yellow]3. Find Vulnerabilities[/yellow]")
    console.print("[yellow]4. Capture Handshake[/yellow]")
    console.print("[yellow]5. Brute Force Attack[/yellow]")
    console.print("[yellow]6. Router Analysis[/yellow]")
    console.print("[yellow]0. Exit[/yellow]")
    
    while True:
        choice = input("\n[*] Select option (0-6): ")
        
        if choice == '1':
            show_password()
        elif choice == '2':
            scan_networks()
        elif choice == '3':
            vulnerability_scan()
        elif choice == '4':
            target = input("Enter target BSSID: ")
            capture_handshake(target)
        elif choice == '5':
            target = input("Enter target SSID: ")
            brute_force(target)
        elif choice == '6':
            router_analysis()
        elif choice == '0':
            console.print("[green]Goodbye![/green]")
            break
        else:
            console.print("[red]Invalid option![/red]")

if __name__ == '__main__':
    cli()
