# FTP Server and Client - Cybersecurity Lab

This project provides a complete FTP server and client implementation for cybersecurity education and network analysis. It allows you to observe unencrypted file transfers in [Wireshark](#📊-wireshark-analysis) and understand FTP protocol behavior.

<br><br>

## 🚨 Security Warning

**This FTP implementation transmits data unencrypted for educational purposes only.** Never use this setup in production environments. Always use encrypted protocols (FTPS/SFTP) for real-world applications.

<br><br>

## 📋 Table of Contents

1. [Features](#✨-features)

   - [FTP Server](#ftp-server)
   - [FTP Client](#ftp-client)
   - [Test Data Generator Script](#test-data-generator-script)

2. [Requirements](#🛠️-requirements)

   - [Running the IDE as Administrator](#⚡-running-the-ide-as-administrator)
   - [Running the FTP Server and Client as Administrators](#🔐-running-the-ftp-server-and-client-as-administrators)

3. [Installation](#📦-installation)

4. [Virtual Environment Setup](#🐍-virtual-environment-setup)

   - [Why Use Virtual Environments?](#why-use-virtual-environments)
   - [Creating and Using Virtual Environment](#creating-and-using-virtual-environment)
   - [Virtual Environment Best Practices](#virtual-environment-best-practices)
   - [IDE Integration](#ide-integration)

5. [Configuration](#⚙️-configuration)

   - [Environment Variables](#environment-variables)
   - [Environment Setup](#environment-setup)
   - [Multi-Machine Setup](#multi-machine-setup)

6. [Windows Firewall Setup](#🔥-windows-firewall-setup)

   - [Creating Firewall Rules](#creating-firewall-rules)
   - [Alternative: Command Line Method](#alternative-command-line-method)

7. [Folder Permissions (Windows)](#📁-folder-permissions-windows)

   - [Using icacls Command](#using-icacls-command)
   - [Permission Parameters Explained](#permission-parameters-explained)
   - [GUI Method](#gui-method)

8. [Usage](#🚀-usage)

   - [Prerequisites](#prerequisites)
   - [Starting the FTP Server](#starting-the-ftp-server)
   - [Using the FTP Client](#using-the-ftp-client)
   - [Creating Test Data](#creating-test-data)

9. [Wireshark Analysis](#📊-wireshark-analysis)

   - [Starting Wireshark Capture](#starting-wireshark-capture)
   - [What to Observe](#what-to-observe)
   - [Sample Wireshark Filters](#sample-wireshark-filters)
   - [Key Security Observations](#key-security-observations)

10. [Troubleshooting](#🔧-troubleshooting)

    - [Virtual Environment Issues](#virtual-environment-issues)
    - [ModuleNotFoundError](#modulenotfounderror)
    - [Server Wonâ€™t Start](#server-wont-start)
    - [Connection Refused](#connection-refused)
    - [Upload/Download Failures](#uploaddownload-failures)
    - [Passive Mode Issues](#passive-mode-issues)
    - [Environment Variables Not Loading](#environment-variables-not-loading)

11. [Lab Exercises](#🎯-lab-exercises)

    - [Exercise 1: Basic Protocol Analysis](#exercise-1-basic-protocol-analysis)
    - [Exercise 2: File Transfer Monitoring](#exercise-2-file-transfer-monitoring)
    - [Exercise 3: Attack Simulation](#exercise-3-attack-simulation)
    - [Exercise 4: Network Reconnaissance](#exercise-4-network-reconnaissance)
    - [Exercise 5: Multi-Machine Setup](#exercise-5-multi-machine-setup)

12. [Cleanup](#🧹-cleanup)

    - [Deactivate Virtual Environment](#1-deactivate-virtual-environment)
    - [Remove Firewall Rules](#2-remove-firewall-rules)
    - [Remove Virtual Environment](#3-remove-virtual-environment-optional)
    - [Remove Server Directory](#4-remove-server-directory-optional)
    - [Clean Log Files](#5-clean-log-files)
    - [Security Verification](#6-security-verification)

13. [Additional Notes](#📝-additional-notes)

    - [Complete Project Structure](#complete-project-structure)
    - [Security Best Practices Learned](#security-best-practices-learned)
    - [Educational Value](#educational-value)

14. [Support](#🆘-support)

<br><br>

## ✨ Features

### [FTP Server](ftp_server.py)

- Custom logging for all FTP operations (connect, login, upload, download, commands)
- DummyAuthorizer for custom credentials (no Windows user dependency)
- Automatic server directory creation with sample structure
- Configurable [permissions](#📁-folder-permissions-windows) and [port settings](#environment-variables)
- Real-time terminal output of all activities
- Comprehensive log file generation

<br>
 
### [FTP Client](ftp_client.py)

- Command-line interface for quick operations
- Interactive shell mode with FTP-like commands
- Support for upload, download, directory listing, and navigation
- [Environment variable](#environment-variables) configuration
- Both single-machine and [multi-machine setup](#multi-machine-setup) support

<br>
 
### [Test Data Generator Script](generate_test_data.py)

- Creates realistic business files (employee records, sales data, system logs)
- Multiple file formats (CSV, JSON, TXT, INI, LOG)
- Dynamic content with randomized data and timestamps
- Varied file sizes for comprehensive FTP testing
- Auto-organized directory structure creation
- Safe fictional data for educational use

<br><br>

## 🛠️ Requirements

- Python 3.7 or higher (current version: 3.13.7)
- Windows, Linux, or macOS
- Administrator privileges (for port binding and [firewall configuration](#🔥-windows-firewall-setup))
- [Wireshark](#📊-wireshark-analysis) (for traffic analysis)

<br><br>

## 📦 Installation

**⚠️ HIGHLY RECOMMENDED:** Run terminal as administrator.

From a terminal (PowerShell, CMD, or bash):

1. Create and move into the project folder:

   ```bash
   mkdir ftp_cybersec_lab
   cd ftp_cybersec_lab
   ```

<br>

2. Clone the repository into the current folder:

   ```bash
   git clone https://github.com/golso4243/python-ftp-server-cybersec-lab .
   ```

   ⚠️ The trailing . makes sure files are cloned directly into ftp_cybersec_lab instead of a nested folder.

<br>

3. Open the project in VS Code: `code .`


   💡 **Tip: Enable the `code` command**  
      - The `code` command lets you open VS Code from your terminal (e.g., with `code .`).
      - On Windows: During installation of VS Code, check **“Add to PATH”** so the `code` command works in PowerShell or CMD.
      - If you missed it, open VS Code, press `Ctrl+Shift+P`, search for **“Shell Command: Install 'code' command in PATH”**, and run it.
      - After this, restart your terminal and you’ll be able to type `code .` to open the current folder (ftp_cybersec_lab) in VS Code.


<br>

4. Set up [virtual environment](#🐍-virtual-environment-setup) **(RECOMMENDED)**

<br>
 
5. Install Python dependencies: `pip install -r requirements.txt`

<br>
 
6. Verify installation: `python -c "import pyftpdlib; print('Dependencies installed successfully')"`

<br><br>

## 🐍 Virtual Environment Setup

**⚠️ HIGHLY RECOMMENDED:** Use a virtual environment to isolate project dependencies and prevent conflicts with system packages.

### Why Use Virtual Environments?

- **Dependency Isolation:** Prevents conflicts between different Python projects
- **Security:** Reduces risk of system-wide package pollution
- **Reproducibility:** Ensures consistent environment across different systems
- **Clean Uninstall:** Easy to remove all project dependencies by deleting the virtual environment

<br>
 
### Creating and Using Virtual Environment

#### Windows:

```bash
# Navigate to project directory
# Skip this step if the project directory is already open in your IDE.
cd ftp_cybersec_lab

# Create virtual environment
python -m venv ftp_lab_venv

# Activate virtual environment
ftp_lab_venv\Scripts\activate

# Verify activation (you should see (ftp_lab_venv) in your prompt)
where python

# Install dependencies
pip install -r requirements.txt

# When done working, deactivate
deactivate
```

<br>
 
#### Linux/macOS:
```bash
# Navigate to project directory
cd ftp_cybersec_lab

# Create virtual environment

python3 -m venv ftp_lab_venv

# Activate virtual environment

source ftp_lab_venv/bin/activate

# Verify activation (you should see (ftp_lab_venv) in your prompt)

which python

# Install dependencies

pip install -r requirements.txt

# When done working, deactivate

deactivate

````

<br>

#### Alternative: Using conda (if installed):
```bash
# Create conda environment
conda create -n ftp_lab_venv python=3.9

# Activate environment
conda activate ftp_lab_venv

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
conda deactivate
````

<br>
 
### Virtual Environment Best Practices

1. **Always activate before working:**

   ```bash
   # Windows
   ftp_lab_venv\Scripts\activate

   # Linux/macOS
   source ftp_lab_venv/bin/activate
   ```

<br>
 
2. **Verify activation:**
   - Your command prompt should show `(ftp_lab_venv)` prefix
   - `python --version` should show your expected Python version
   - `pip list` should show only project dependencies
 
<br>
 
3. **Update requirements.txt after adding packages:** `pip freeze > requirements.txt`
 
<br>
 
4. **Recreate environment from scratch (if needed):**
   ```bash
   # Windows
   # If "rmdir" command does not work > close IDE, delete from folder, reopen IDE, recreate virtual environment
   rmdir /s ftp_lab_venv
   python -m venv ftp_lab_venv
   ftp_lab_venv\Scripts\activate
   pip install -r requirements.txt
   
   # Linux/macOS
   rm -rf ftp_lab_venv
   python3 -m venv ftp_lab_venv
   source ftp_lab_venv/bin/activate
   pip install -r requirements.txt
   ```
 
<br>
 
### IDE Integration

#### VS Code:

1. Open project folder in VS Code
2. Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
3. Type "Python: Select Interpreter"
4. Choose the interpreter from your [virtual environment](#creating-and-using-virtual-environment):
   - Windows: `ftp_lab_venv\Scripts\python.exe`
   - Linux/macOS: `ftp_lab_venv/bin/python`

<br>
 
#### PyCharm:
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing Environment"
4. Browse to your [virtual environment's](#creating-and-using-virtual-environment) Python executable

<br><br>

## ⚙️ Configuration

### Environment Variables

The project uses `.env.development` for configuration.
Default settings:

```env
FTP_HOST=127.0.0.1          # Server IP address
FTP_PORT=2121               # FTP port (non-standard for lab safety)
FTP_USER=labuser            # FTP username
FTP_PASSWORD=labpass123     # FTP password
FTP_SERVER_ROOT=ftp_server_root  # Server directory name
FTP_PERMISSIONS=elradfmwMT  # User permissions
```

<br>

### Environment Setup

Before running the application, make sure to set up your environment variables.

Copy the development environment `.env.development` file to `.env`:

### Linux / macOS / Git Bash

```bash
cp .env.development .env
```

<br>

### Windows (PowerShell or Command Prompt)

```powershell
copy .env.development .env
```

<br>

You can delete the `.env.development` afterwards.

<br>
 
### Multi-Machine Setup

For testing across different machines:

1. **On the server machine:**
   - Change `FTP_HOST=0.0.0.0` in `.env` to bind to all interfaces
   - Note the server's IP address (e.g., `ipconfig` on Windows, `ip addr` on Linux)

<br>
 
2. **On the client machine:**
   - Change `FTP_HOST=<server-ip-address>` in `.env`
   - Example: `FTP_HOST=192.168.1.100`

<br><br>

## 🔥 Windows Firewall Setup

**⚠️ CRITICAL: Always disable or delete these rules after [lab completion](#🧹-cleanup) for security!**

### Creating Firewall Rules

1. **Open Windows Defender Firewall with Advanced Security:**
   - Press `Win + R`, type `wf.msc`, press Enter
   - Or search "Windows Defender Firewall with Advanced Security"

<br>
 
2. **Create Inbound Rule:**
   ```
   - Right-click "Inbound Rules" → "New Rule..."
   - Rule Type: Port
   - Protocol: TCP
   - Specific Local Ports: 2121
   - Action: Allow the connection
   - Profile: Check all (Domain, Private, Public)
   - Name: "FTP Lab Server Port 2121"
   - Description: "Temporary rule for cybersecurity lab - DELETE AFTER USE"
   ```
 
<br>
 
3. **Create Outbound Rule:**
   ```
   - Right-click "Outbound Rules" → "New Rule..."
   - Rule Type: Port
   - Protocol: TCP
   - Specific Local Ports: 2121
   - Action: Allow the connection
   - Profile: Check all (Domain, Private, Public)
   - Name: "FTP Lab Client Port 2121"
   - Description: "Temporary rule for cybersecurity lab - DELETE AFTER USE"
   ```
 
<br>
 
4. **Allow FTP Data Ports (Passive Mode):**
   ```
   - Create additional inbound/outbound rules for ports 60000-65535
   - Or create a rule for "FTP Server" program instead
   ```
 
<br>
 
### Alternative: Command Line Method

Run as Administrator:

```powershell
# Allow inbound FTP control port
netsh advfirewall firewall add rule name="FTP Lab Inbound" dir=in action=allow protocol=TCP localport=2121

# Allow outbound FTP control port
netsh advfirewall firewall add rule name="FTP Lab Outbound" dir=out action=allow protocol=TCP localport=2121

# Allow passive data ports (optional - for better compatibility)
netsh advfirewall firewall add rule name="FTP Lab Data Ports" dir=in action=allow protocol=TCP localport=60000-65535
```

<br><br>

## 📁 Folder Permissions (Windows)

### Using icacls Command

If you encounter permission issues with the FTP server directory:

```powershell
# Grant full control to the current user
icacls ftp_server_root /grant %USERNAME%:F /T

# Grant read/write permissions to specific user
icacls ftp_server_root /grant "labuser":(OI)(CI)RX /T

# View current permissions
icacls ftp_server_root

# Reset permissions to defaults (if needed)
icacls ftp_server_root /reset /T

# Grant permissions to Everyone (least secure - only for isolated lab)
icacls ftp_server_root /grant Everyone:F /T
```

<br>
 
### Permission Parameters Explained:
- `F` = Full control
- `RX` = Read and execute
- `RW` = Read and write
- `(OI)` = Object inherit
- `(CI)` = Container inherit
- `/T` = Apply to all files and subdirectories
 
<br>
 
### GUI Method:
1. Right-click `ftp_server_root` folder → Properties
2. Security tab → Edit → Add
3. Enter "Everyone" or specific username
4. Grant "Full control" permissions
5. Apply to subfolders and files

<br><br>

## 🚀 Usage

### Prerequisites

**⚠️ IMPORTANT: Always activate your [virtual environment](#creating-and-using-virtual-environment) before running scripts!**

```bash
# Windows
ftp_lab_venv\Scripts\activate

# Linux/macOS
source ftp_lab_venv/bin/activate
```

<br>
 
### Starting the FTP Server

```bash
python ftp_server.py
```

Expected output:

```
============================================================
           FTP SERVER - CYBERSECURITY LAB
============================================================
Server Host: 127.0.0.1
Server Port: 2121
Username: labuser
Password: labpass123
Server Root: ftp_server_root
Permissions: elradfmwMT
Log File: logs/ftp_server_20240904_143022.log
============================================================

[2024-09-04 14:30:22] Starting FTP server...
Server listening on 127.0.0.1:2121
Press Ctrl+C to stop the server

WARNING: This server transmits data unencrypted for lab purposes!
Monitor traffic with Wireshark on port 2121
------------------------------------------------------------
```

Confirm FTP services running: `netstat -an | findstr 2121`

<br>
 
### Using the FTP Client

#### Interactive Mode:

```bash
python ftp_client.py
```

Interactive commands:

```
FTP> help                    # Show all commands
FTP> ls                      # List current directory
FTP> upload test.txt         # Upload file
FTP> download welcome.txt    # Download file
FTP> cd uploads             # Change directory
FTP> pwd                    # Show current directory
FTP> stats                  # Show connection status
FTP> quit                   # Exit client
```

<br>
 
#### Command Line Mode:

```bash
# Upload files
python ftp_client.py upload local_file.txt
python ftp_client.py upload ftp_test_data/app_config.json uploads/config.json

# Download files
python ftp_client.py download welcome.txt
python ftp_client.py download uploads/config.json local_config.json

# List directories
python ftp_client.py ls
python ftp_client.py ls uploads

# Connect to different server
python ftp_client.py connect 192.168.1.100 2121 testuser testpass
```

<br>
 
### Creating Test Data

Use the provided [test data generator script](#test-data-generator-script) to create realistic files for testing: `python generate_test_data.py`

<br>
 
This will create the `ftp_test_data/` directory in the root folder with the following files:

- **`employee_records.csv`** - Employee database records (CSV format)
- **`app_config.json`** - Application configuration (JSON format)
- **`sales_data.csv`** - Sales transaction data (CSV format)
- **`system.log`** - System activity logs (LOG format)
- **`project_documentation.txt`** - Project documentation (TXT format)
- **`network_config.ini`** - Network configuration (INI format)

The generator creates realistic test data with various file formats and sizes, perfect for comprehensive FTP testing. All data is fictional and safe for educational use.

<br>
 
**Manual Creation (Alternative):**
If you prefer to create test files manually:

```bash
mkdir ftp_test_data
echo "This is a test file for FTP transfer" > ftp_test_data/test.txt
echo "Sensitive document content here" > ftp_test_data/confidential.txt
```

<br><br>

## 📊 Wireshark Analysis

### Starting Wireshark Capture

1. Open Wireshark

<br>

2. Select Network Interface:

   ```
   - For localhost: Select "Loopback" or "lo0"
   - For network: Select your network adapter
   ```

<br>

3. **Apply Filter:** `tcp.port == 2121` or `ftp` or `ftp-data`

<br>

4. Start Capture

<br>

### What to Observe

#### FTP Control Channel (Port 2121):

- **Connection establishment:** TCP 3-way handshake
- **Authentication:** USER and PASS commands in plaintext
- **Commands:** LIST, PWD, CWD, STOR, RETR commands
- **Responses:** Server response codes (220, 230, 150, 226, etc.)

<br>

#### FTP Data Channel (Ephemeral Ports):

- **File content:** Complete file data in plaintext
- **Directory listings:** Detailed file information
- **Passive mode setup:** PASV command and data port negotiation

<br>

### Sample Wireshark Filters:

```
# FTP commands only
ftp.request

# FTP responses only

ftp.response

# File transfer data

ftp-data

# Specific file transfers

ftp-data and tcp contains "filename"

# Authentication attempts

ftp.request.command == "USER" or ftp.request.command == "PASS"

```

<br>

### Key Security Observations:

1. **Credentials transmitted in plaintext**
2. **File contents visible without encryption**
3. **Directory structure exposed**
4. **No integrity protection**

<br><br>

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Virtual Environment Issues

```

Error: 'python' is not recognized as an internal or external command

```

**Solution:** Activate [virtual environment](#creating-and-using-virtual-environment) first:

```bash
# Windows
ftp_lab_venv\Scripts\activate

# Linux/macOS
source ftp_lab_venv/bin/activate
```

<br>
 
#### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'pyftpdlib'
```
**Solutions:**
- Ensure [virtual environment](#creating-and-using-virtual-environment) is activated
- Install dependencies: `pip install -r requirements.txt`
- Verify you're in the correct environment: `pip list`
 
<br>
 
#### Server Won't Start
```
Error: Permission denied to bind to port 2121
```
**Solution:** Run as administrator or use a port > 1024
 
<br>
 
#### Connection Refused
```
Connection failed: [Errno 10061] No connection could be made
```
**Solutions:**
- Check if [server is running](#starting-the-ftp-server)
- Verify [firewall rules](#🔥-windows-firewall-setup)
- Confirm correct IP/port in [configuration](#⚙️-configuration)
- Try `telnet 127.0.0.1 2121` to test basic connectivity
 
<br>
 
#### Upload/Download Failures
```
Upload failed: 550 Permission denied
```
**Solutions:**
- Check [folder permissions](#📁-folder-permissions-windows) with `icacls`
- Verify FTP_PERMISSIONS in [`.env`](#environment-variables)
- Ensure server directory exists and is writable
 
<br>
 
#### Passive Mode Issues
```
425 Can't open data connection
```
**Solutions:**
- Configure [firewall](#🔥-windows-firewall-setup) for passive ports (60000-65535)
- Check router/NAT settings for [multi-machine setup](#multi-machine-setup)
- Try active mode (less common)
 
<br>
 
#### Environment Variables Not Loading
**Solutions:**
- Verify [`.env` file](#environment-setup) exists
- Check file encoding (should be UTF-8)
- Ensure no spaces around `=` in env file

<br><br>

## 🎯 Lab Exercises

### Exercise 1: Basic Protocol Analysis

1. Start [server](#starting-the-ftp-server) and capture traffic
2. Connect [client](#using-the-ftp-client) and authenticate
3. **Analyze:** Find credentials in packet capture
4. **Question:** How could this be secured?

<br>
 
### Exercise 2: File Transfer Monitoring
1. Upload a text file with sensitive content
2. Download the same file
3. **Analyze:** Locate file content in packets
4. **Question:** What data leakage risks exist?
 
<br>
 
### Exercise 3: Attack Simulation
1. Use wrong credentials multiple times
2. Observe server logs and [Wireshark](#📊-wireshark-analysis)
3. **Analyze:** How are failed attempts logged?
4. **Question:** What brute force indicators exist?
 
<br>
 
### Exercise 4: Network Reconnaissance
1. Use different FTP commands (LIST, PWD, CWD)
2. **Analyze:** What system information is revealed?
3. **Question:** How could an attacker map the system?
 
<br>
 
### Exercise 5: Multi-Machine Setup
1. Configure [server on one machine, client on another](#multi-machine-setup)
2. Analyze traffic between machines
3. **Question:** What additional network risks appear?

<br><br>

## 🧹 Cleanup

### After Lab Completion

#### 1. Deactivate Virtual Environment

```bash
deactivate
```

<br>
 
#### 2. Remove Firewall Rules
**GUI Method:**
- Open Windows Defender Firewall with Advanced Security
- Delete "FTP Lab Server Port 2121" rules
- Delete "FTP Lab Client Port 2121" rules
- Delete any passive port rules created
 
<br>
 
**Command Line Method:**
```cmd
# Remove firewall rules
netsh advfirewall firewall delete rule name="FTP Lab Inbound"
netsh advfirewall firewall delete rule name="FTP Lab Outbound"  
netsh advfirewall firewall delete rule name="FTP Lab Data Ports"
```
 
<br>
 
#### 3. Remove Virtual Environment (Optional)
```bash
# Windows
rmdir /s ftp_lab_venv

# Linux/macOS

rm -rf ftp_lab_venv

````

<br>

#### 4. Remove Server Directory (Optional)
```bash
# Windows
rmdir /s ftp_server_root

# Linux/Mac
rm -rf ftp_server_root
````

<br>
 
#### 5. Clean Log Files
```bash
# Remove all log files
rmdir /s logs       # Windows
rm -rf logs         # Linux/Mac
```
 
<br>
 
#### 6. Security Verification

- Confirm no FTP services running: `netstat -an | findstr 2121`

- Verify [firewall rules](#🔥-windows-firewall-setup) removed

- Check for any remaining test files with sensitive content

<br><br>

## 📝 Additional Notes

### Complete Project Structure

```
ftp_cybersec_lab/
├── ftp_server.py              # Main server application
├── ftp_client.py              # Main client application
├── generate_test_data.py      # Test data generator script
├── .env                       # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── ftp_lab_venv/              # Virtual environment (created by user)
├── ftp_server_root/           # Server directory (auto-created)
│   ├── uploads/               # Upload destination
│   ├── downloads/             # Download source
│   ├── shared/                # Shared files
│   └── welcome.txt            # Sample file
├── ftp_test_data/             # Test files (generated)
│   ├── employee_records.csv
│   ├── app_config.json
│   ├── sales_data.csv
│   ├── system.log
│   ├── project_documentation.txt
│   └── network_config.ini
└── logs/                      # Server logs (auto-created)
    └── ftp_server_*.log       # Timestamped log files
```

<br>
 
### Security Best Practices Learned
1. **Never use unencrypted FTP in production**
2. **Always use strong authentication mechanisms**
3. **Implement proper access controls and [permissions](#📁-folder-permissions-windows)**
4. **Monitor and log all file transfer activities**
5. **Use encrypted protocols (FTPS/SFTP) for real applications**
6. **Regularly audit [firewall rules](#🔥-windows-firewall-setup) and network access**
7. **Use [virtual environments](#🐍-virtual-environment-setup) to isolate project dependencies**
 
<br>
 
### Educational Value
This lab demonstrates:
- Network protocol analysis techniques
- Plaintext credential interception
- File transfer security risks
- [Firewall configuration](#🔥-windows-firewall-setup) importance
- System monitoring and logging
- Cybersecurity threat vectors
- Python development best practices

<br>

## 🆘 Support

If you encounter issues:

1. Ensure [virtual environment](#creating-and-using-virtual-environment) is activated
2. Check the [troubleshooting](#🔧-troubleshooting) section above
3. Verify all [prerequisites](#prerequisites) are met
4. Review [firewall](#🔥-windows-firewall-setup) and [permissions](#📁-folder-permissions-windows) settings
5. Check server and client logs for detailed error messages

<br><br>

**Remember:** This is for educational purposes only. Always prioritize security in real-world applications!
