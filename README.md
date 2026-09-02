# WiFi Security Analyzer 🔒

**Advanced Router Security Scanner** - WiFi Password Finder, Vulnerability Detection, Network Analysis

## Features ✨

- 🔍 WiFi Network Discovery & Scanning
- 🔐 Current WiFi Password Display
- 🎯 Router Vulnerability Detection
- 🚨 Security Holes Identification
- 🤝 WPA/WPA2 Handshake Capture
- 💥 Dictionary & Brute Force Attack
- 🖥️ GUI Interface (Python Tkinter)
- 💻 CLI Tools (Windows CMD)
- 📊 Detailed Security Reports
- ⚙️ Router Configuration Analysis

## Requirements

### Windows Requirements
- Windows 7/10/11
- Python 3.8+
- Visual C++ 2019 Redistributable
- Administrator Privileges

### Python Dependencies
```bash
pip install -r requirements.txt
```

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/rezab1706-cell/wifi-security-analyzer.git
cd wifi-security-analyzer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run with Administrator
```bash
# GUI Mode
python main_gui.py

# CLI Mode
python main_cli.py
```

## Usage

### GUI Mode
1. Run `python main_gui.py`
2. Select desired operation
3. Click Start
4. View results in output panel

### CLI Mode
```bash
# Show current WiFi password
python main_cli.py --show-password

# Scan networks
python main_cli.py --scan-networks

# Find vulnerabilities
python main_cli.py --vulnerability-scan

# Capture handshake
python main_cli.py --capture-handshake --target <BSSID>

# Brute force attack
python main_cli.py --brute-force --target <SSID>
```

## File Structure
```
wifi-security-analyzer/
├── main_gui.py              # GUI Application
├── main_cli.py              # CLI Application
├── requirements.txt         # Python Dependencies
├── config.py               # Configuration
├── modules/
│   ├── wifi_scanner.py     # Network Scanning
│   ├── password_extractor.py # Password Extraction
│   ├── vulnerability_scanner.py # Vulnerability Detection
│   ├── handshake_capture.py   # Handshake Capture
│   ├── brute_force.py        # Brute Force Attack
│   ├── router_analyzer.py    # Router Analysis
│   └── report_generator.py   # Report Generation
└── utils/
    ├── logger.py            # Logging
    └── helpers.py           # Helper Functions
```

## ⚠️ Legal Disclaimer

This tool is for **educational and authorized security testing only**. Unauthorized access to computer networks is illegal. Always obtain proper authorization before performing security tests.

## License

MIT License - See LICENSE file for details

## Author

**Reza** - rezab1706-cell

---

**⭐ Star this repo if you find it useful!**
