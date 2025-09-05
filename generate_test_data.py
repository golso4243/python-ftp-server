#!/usr/bin/env python3
"""
📁 FTP Test Data Generator
Creates demo files for FTP server and client testing
"""

import os
import json
import csv
import argparse
from datetime import datetime, timedelta
import random


def create_test_directory():
    """📂 Create test data directory"""

    test_dir = "ftp_test_data"
    try:
        if not os.path.exists(test_dir):
            os.makedirs(test_dir)
            print(f"📁 Created directory: {test_dir}")
        else:
            print(f"📁 Using existing directory: {test_dir}")
        return test_dir
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return None


def generate_employee_csv(test_dir):
    """👥 Generate employee records CSV file"""

    filename = os.path.join(test_dir, "employee_records.csv")
    try:
        employees = [
            ["ID", "Name", "Department", "Email", "Salary", "Hire_Date"],
            ["001", "Alice Johnson", "Engineering",
                "alice.johnson@company.com", "75000", "2022-03-15"],
            ["002", "Bob Smith", "Marketing",
                "bob.smith@company.com", "65000", "2021-08-22"],
            ["003", "Carol Williams", "HR",
                "carol.williams@company.com", "58000", "2020-11-10"],
            ["004", "David Brown", "Engineering",
                "david.brown@company.com", "82000", "2019-05-18"],
            ["005", "Eva Davis", "Sales",
                "eva.davis@company.com", "72000", "2023-01-09"],
            ["006", "Frank Miller", "IT Support",
                "frank.miller@company.com", "55000", "2022-07-03"],
            ["007", "Grace Wilson", "Finance",
                "grace.wilson@company.com", "68000", "2021-12-14"],
            ["008", "Henry Taylor", "Engineering",
                "henry.taylor@company.com", "79000", "2020-09-28"]
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(employees)

        print(
            f"✅ Created: employee_records.csv ({len(employees)-1} employees)")
        return True
    except Exception as e:
        print(f"❌ Error creating employee CSV: {e}")
        return False


def generate_config_json(test_dir):
    """⚙️ Generate application configuration JSON file"""

    filename = os.path.join(test_dir, "app_config.json")
    try:
        config = {
            "application": {
                "name": "FTP Demo Application",
                "version": "1.0.0",
                "environment": "development",
                "debug_mode": True
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "demo_db",
                "username": "demo_user",
                "connection_pool_size": 10,
                "timeout": 30
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8080,
                "ssl_enabled": False,
                "max_connections": 100,
                "request_timeout": 60
            },
            "logging": {
                "level": "INFO",
                "file": "/var/log/app.log",
                "max_size_mb": 100,
                "backup_count": 5,
                "console_output": True
            },
            "features": {
                "user_authentication": True,
                "file_upload": True,
                "email_notifications": False,
                "analytics": True,
                "cache_enabled": True
            }
        }

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)

        print(f"✅ Created: app_config.json (application configuration)")
        return True
    except Exception as e:
        print(f"❌ Error creating config JSON: {e}")
        return False


def generate_sales_data_csv(test_dir):
    """📊 Generate sales data CSV file"""

    filename = os.path.join(test_dir, "sales_data.csv")
    try:
        # Generate sample sales data for the last 30 days
        sales_data = [["Date", "Product", "Quantity",
                       "Unit_Price", "Total", "Salesperson"]]

        products = ["Widget A", "Widget B", "Gadget X",
                    "Gadget Y", "Tool Pro", "Tool Lite"]
        salespeople = ["John Doe", "Jane Smith",
                       "Mike Johnson", "Sarah Wilson", "Tom Brown"]

        base_date = datetime.now() - timedelta(days=30)

        for day in range(30):
            current_date = base_date + timedelta(days=day)
            # Generate 2-5 sales per day
            daily_sales = random.randint(2, 5)

            for _ in range(daily_sales):
                product = random.choice(products)
                quantity = random.randint(1, 10)
                unit_price = round(random.uniform(19.99, 299.99), 2)
                total = round(quantity * unit_price, 2)
                salesperson = random.choice(salespeople)

                sales_data.append([
                    current_date.strftime("%Y-%m-%d"),
                    product,
                    quantity,
                    unit_price,
                    total,
                    salesperson
                ])

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(sales_data)

        print(f"✅ Created: sales_data.csv ({len(sales_data)-1} sales records)")
        return True
    except Exception as e:
        print(f"❌ Error creating sales CSV: {e}")
        return False


def generate_system_log(test_dir):
    """📋 Generate system log file"""

    filename = os.path.join(test_dir, "system.log")
    try:
        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        components = ["Database", "WebServer",
                      "Authentication", "FileSystem", "Network"]

        log_entries = []
        base_time = datetime.now() - timedelta(hours=24)

        # Generate 50 log entries over the last 24 hours
        for i in range(50):
            # Random time in 24 hours
            timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
            level = random.choice(log_levels)
            component = random.choice(components)

            # Generate appropriate messages based on level
            if level == "ERROR":
                messages = [
                    f"{component}: Connection timeout occurred",
                    f"{component}: Failed to process request",
                    f"{component}: Access denied for user",
                    f"{component}: Resource not available"
                ]
            elif level == "WARNING":
                messages = [
                    f"{component}: High memory usage detected",
                    f"{component}: Slow response time",
                    f"{component}: Deprecated function called",
                    f"{component}: Cache miss rate high"
                ]
            elif level == "INFO":
                messages = [
                    f"{component}: Service started successfully",
                    f"{component}: User logged in",
                    f"{component}: File processed",
                    f"{component}: Backup completed"
                ]
            else:  # DEBUG
                messages = [
                    f"{component}: Processing request ID {random.randint(1000, 9999)}",
                    f"{component}: Cache hit for key {random.randint(100, 999)}",
                    f"{component}: Function executed in {random.randint(10, 500)}ms",
                    f"{component}: Memory usage: {random.randint(50, 90)}%"
                ]

            message = random.choice(messages)
            log_entry = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {message}"
            log_entries.append(log_entry)

        # Sort by timestamp
        log_entries.sort()

        with open(filename, 'w', encoding='utf-8') as file:
            for entry in log_entries:
                file.write(entry + '\n')

        print(f"✅ Created: system.log ({len(log_entries)} log entries)")
        return True
    except Exception as e:
        print(f"❌ Error creating system log: {e}")
        return False


def generate_readme_doc(test_dir):
    """📖 Generate project documentation file"""

    filename = os.path.join(test_dir, "project_documentation.txt")
    try:
        content = """🚀 PROJECT DOCUMENTATION
========================

📝 Project Overview
-------------------
This is a sample project documentation file created for FTP testing purposes.
It demonstrates how various file types can be transferred using FTP protocols.

🎯 Objectives
-------------
- Test FTP file transfer capabilities
- Demonstrate handling of different file formats
- Provide realistic data for network lab exercises
- Showcase proper documentation practices

📊 Test Data Contents
---------------------
1. employee_records.csv - Employee database records
2. app_config.json - Application configuration settings
3. sales_data.csv - Monthly sales transaction data
4. system.log - System activity and error logs
5. project_documentation.txt - This documentation file

🔧 Technical Specifications
---------------------------
- File Encoding: UTF-8
- CSV Format: RFC 4180 compliant
- JSON Format: Valid JSON with proper indentation
- Log Format: Standard timestamp + level + message
- Documentation: Plain text with emoji formatting

🚨 Security Notes
-----------------
- All data is fictional and for testing purposes only
- Do not use real employee or customer information
- Ensure proper network isolation during testing
- Remove test data after lab completion

📅 File Generation Details
--------------------------
Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
Python Version: 3.x
Purpose: FTP Protocol Testing and Education

🤝 Usage Instructions
---------------------
1. Use these files to test FTP upload functionality
2. Download files to verify FTP client operations
3. Test directory navigation with the FTP client
4. Verify file integrity after transfer

⚡ Performance Testing
---------------------
- Small files: < 1KB (config files)
- Medium files: 1-10KB (CSV data, logs)
- Text files: Various formats and encodings
- Mixed content: Structured and unstructured data

🎓 Educational Value
--------------------
This test data set provides realistic examples of:
- Database exports (CSV format)
- Configuration management (JSON)
- System monitoring (log files)
- Documentation practices (text files)
- File transfer protocols (FTP)

---
End of Documentation
"""

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"✅ Created: project_documentation.txt (comprehensive documentation)")
        return True
    except Exception as e:
        print(f"❌ Error creating documentation: {e}")
        return False


def generate_network_config(test_dir):
    """🌐 Generate network configuration file"""

    filename = os.path.join(test_dir, "network_config.ini")
    try:
        config_content = """# 🌐 Network Configuration File
# Generated for FTP Testing Purposes
# DO NOT USE IN PRODUCTION

[NETWORK]
# Primary network settings
interface=eth0
ip_address=192.168.1.100
subnet_mask=255.255.255.0
gateway=192.168.1.1
dns_primary=8.8.8.8
dns_secondary=8.8.4.4
mtu=1500

[FTP_SERVER]
# FTP server configuration
enabled=true
port=21
passive_mode=true
data_port_range=20000-20100
max_connections=50
timeout=300
welcome_message="Welcome to Demo FTP Server"

[SECURITY]
# Security settings
firewall_enabled=true
allowed_ips=192.168.1.0/24
blocked_ips=
encryption=none
anonymous_access=false
max_login_attempts=3
session_timeout=1800

[LOGGING]
# Logging configuration
log_level=INFO
log_file=/var/log/ftp.log
log_rotation=daily
max_log_size=10MB
retain_logs=30

[PERFORMANCE]
# Performance tuning
buffer_size=8192
concurrent_transfers=10
bandwidth_limit=0
compression=false
keepalive=true
keepalive_interval=60

[DIRECTORIES]
# Directory settings
home_directory=/ftp/home
upload_directory=/ftp/uploads
public_directory=/ftp/public
temp_directory=/ftp/temp
max_file_size=100MB
"""

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(config_content)

        print(f"✅ Created: network_config.ini (network configuration)")
        return True
    except Exception as e:
        print(f"❌ Error creating network config: {e}")
        return False


def display_summary(test_dir):
    """📋 Display summary of created files"""

    try:
        files = os.listdir(test_dir)
        total_size = 0

        print("\n" + "="*60)
        print("📊 TEST DATA GENERATION SUMMARY")
        print("="*60)
        print(f"📁 Directory: {test_dir}")
        print(f"📄 Files created: {len(files)}")
        print("-"*60)

        for file in sorted(files):
            filepath = os.path.join(test_dir, file)
            size = os.path.getsize(filepath)
            total_size += size
            size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            print(f"  📄 {file:<25} {size_str:>10}")

        print("-"*60)
        total_size_str = f"{total_size:,} bytes" if total_size < 1024 else f"{total_size/1024:.1f} KB"
        print(f"📦 Total size: {total_size_str}")

        print("\n🎯 Ready for FTP testing!")
        print("✅ Upload these files to your FTP server")
        print("✅ Download them with your FTP client")
        print("✅ Test different file formats and sizes")

    except Exception as e:
        print(f"❌ Error generating summary: {e}")


def show_help():
    """❓ Display help information"""

    help_text = """
📁 FTP Test Data Generator Help
==============================

This script creates realistic test files for FTP server and client testing.

🚀 Usage:
  python generate_test_data.py           # Generate all test files
  python generate_test_data.py --help    # Show this help

📄 Generated Files:
  employee_records.csv       - Employee database records (CSV format)
  app_config.json           - Application configuration (JSON format)
  sales_data.csv            - Sales transaction data (CSV format)
  system.log                - System activity logs (LOG format)
  project_documentation.txt - Project documentation (TXT format)
  network_config.ini        - Network configuration (INI format)

📁 Output Directory:
  ftp_test_data/            - All files created in this directory

✅ Perfect for testing:
  - FTP file upload/download
  - Different file formats
  - Various file sizes
  - Directory navigation
  - File transfer integrity

⚠️  Note: All data is fictional and for testing purposes only.
"""
    print(help_text)


def main():
    """🎯 Main function to generate test data"""

    # Setup command line argument parsing
    parser = argparse.ArgumentParser(
        description='Generate FTP Test Data', add_help=False)
    parser.add_argument('--help', action='store_true',
                        help='Show help message')
    args = parser.parse_args()

    # Show help if requested
    if args.help:
        show_help()
        return

    print("📁 FTP Test Data Generator")
    print("="*50)

    # Create test directory
    test_dir = create_test_directory()
    if not test_dir:
        print("❌ Failed to create test directory. Exiting...")
        return

    print(f"📂 Generating test files in: {test_dir}")
    print("-"*50)

    # Generate all test files
    success_count = 0
    generators = [
        ("Employee Records", generate_employee_csv),
        ("Configuration File", generate_config_json),
        ("Sales Data", generate_sales_data_csv),
        ("System Log", generate_system_log),
        ("Documentation", generate_readme_doc),
        ("Network Config", generate_network_config)
    ]

    for name, generator in generators:
        print(f"🔄 Generating {name}...")
        if generator(test_dir):
            success_count += 1
        print()

    # Display summary
    print(f"✅ Successfully created {success_count}/{len(generators)} files")
    display_summary(test_dir)

    if success_count == len(generators):
        print("\n🎉 All test files generated successfully!")
        print("🚀 Ready to start FTP testing!")
    else:
        print(
            f"\n⚠️  {len(generators) - success_count} files failed to generate")


if __name__ == "__main__":
    main()
