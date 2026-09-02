#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report Generator Module
Generates security analysis reports
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import os

class ReportGenerator:
    def __init__(self, output_dir: str = "output/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_json_report(self, data: Dict, filename: str = None) -> str:
        """
        Generate JSON report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"[+] JSON report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"[!] Error generating JSON report: {str(e)}")
            return ""
    
    def generate_csv_report(self, data: List[Dict], filename: str = None) -> str:
        """
        Generate CSV report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = self.output_dir / filename
        
        try:
            if not data:
                return ""
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            
            print(f"[+] CSV report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"[!] Error generating CSV report: {str(e)}")
            return ""
    
    def generate_html_report(self, data: Dict, filename: str = None) -> str:
        """
        Generate HTML report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = self.output_dir / filename
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>WiFi Security Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                .critical {{ background-color: #ffcccc; }}
                .high {{ background-color: #ffe6cc; }}
                .medium {{ background-color: #ffffcc; }}
            </style>
        </head>
        <body>
            <h1>WiFi Security Analysis Report</h1>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <h2>Analysis Results</h2>
            <pre>{json.dumps(data, indent=2, default=str)}</pre>
        </body>
        </html>
        """
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"[+] HTML report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"[!] Error generating HTML report: {str(e)}")
            return ""
    
    def generate_text_report(self, data: Dict, filename: str = None) -> str:
        """
        Generate text report
        """
        if filename is None:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("WiFi SECURITY ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                self._write_dict_to_file(f, data, indent=0)
            
            print(f"[+] Text report generated: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"[!] Error generating text report: {str(e)}")
            return ""
    
    def _write_dict_to_file(self, file, data: Dict, indent: int = 0) -> None:
        """
        Recursively write dictionary to file
        """
        indent_str = "  " * indent
        
        for key, value in data.items():
            if isinstance(value, dict):
                file.write(f"{indent_str}{key}:\n")
                self._write_dict_to_file(file, value, indent + 1)
            elif isinstance(value, list):
                file.write(f"{indent_str}{key}:\n")
                for item in value:
                    if isinstance(item, dict):
                        self._write_dict_to_file(file, item, indent + 1)
                    else:
                        file.write(f"{indent_str}  - {item}\n")
            else:
                file.write(f"{indent_str}{key}: {value}\n")
