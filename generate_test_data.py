#!/usr/bin/env python3
"""
FTP Test Data Generator - Refactored Version
Creates demo files for FTP server and client testing
"""

import os
import json
import csv
import argparse
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from typing import List, Dict, Any, Callable


@dataclass
class FileGenerator:
    """Data class for file generator configuration"""

    name: str
    filename: str
    generator_func: Callable
    description: str


class FTPTestDataGenerator:
    """Main class for generating FTP test data"""

    def __init__(self, output_dir: str = "ftp_test_data"):
        self.output_dir = output_dir
        self.success_count = 0

        # Configure all generators
        self.generators = [
            FileGenerator("Employee Records", "employee_records.csv",
                          self._generate_employee_csv, "Employee database records"),
            FileGenerator("App Config", "app_config.json",
                          self._generate_config_json, "Application configuration"),
            FileGenerator("Sales Data", "sales_data.csv",
                          self._generate_sales_csv, "Sales transaction data"),
            FileGenerator("System Log", "system.log",
                          self._generate_system_log, "System activity logs"),
            FileGenerator("Documentation", "README.txt",
                          self._generate_readme, "Project documentation"),
            FileGenerator("Network Config", "network_config.ini",
                          self._generate_network_config, "Network configuration")
        ]

    def create_output_directory(self) -> bool:
        """Create output directory if it doesn't exist"""

        try:
            os.makedirs(self.output_dir, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False

    def _write_csv(self, filename: str, data: List[List[str]]) -> bool:
        """Helper to write CSV data"""

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerows(data)
            return True
        except Exception as e:
            print(f"Error writing CSV {filename}: {e}")
            return False

    def _write_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Helper to write JSON data"""

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing JSON {filename}: {e}")
            return False

    def _write_text(self, filename: str, content: str) -> bool:
        """Helper to write text content"""

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing text {filename}: {e}")
            return False

    def _generate_employee_csv(self, filepath: str) -> bool:
        """Generate employee records CSV"""

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
        ]
        return self._write_csv(filepath, employees)

    def _generate_config_json(self, filepath: str) -> bool:
        """Generate application configuration JSON"""

        config = {
            "app": {"name": "FTP Demo", "version": "1.0.0", "debug": True},
            "database": {"host": "localhost", "port": 5432, "name": "demo_db"},
            "server": {"host": "0.0.0.0", "port": 8080, "ssl": False},
            "features": {"auth": True, "upload": True, "analytics": True}
        }
        return self._write_json(filepath, config)

    def _generate_sales_csv(self, filepath: str) -> bool:
        """Generate sales data CSV"""

        sales_data = [["Date", "Product", "Quantity",
                       "Price", "Total", "Salesperson"]]

        products = ["Widget A", "Widget B", "Gadget X", "Tool Pro"]
        salespeople = ["John Doe", "Jane Smith", "Mike Johnson"]
        base_date = datetime.now() - timedelta(days=30)

        for day in range(30):
            date = (base_date + timedelta(days=day)).strftime("%Y-%m-%d")
            for _ in range(random.randint(1, 3)):
                quantity = random.randint(1, 5)
                price = round(random.uniform(20, 200), 2)
                sales_data.append([
                    date, random.choice(products), quantity, price,
                    round(quantity * price, 2), random.choice(salespeople)
                ])

        return self._write_csv(filepath, sales_data)

    def _generate_system_log(self, filepath: str) -> bool:
        """Generate system log file"""

        log_entries = []
        levels = ["INFO", "WARNING", "ERROR"]
        components = ["Database", "WebServer", "Auth"]

        base_time = datetime.now() - timedelta(hours=24)

        for i in range(20):
            timestamp = base_time + timedelta(minutes=random.randint(0, 1440))
            level = random.choice(levels)
            component = random.choice(components)

            messages = {
                "INFO": f"{component}: Service started",
                "WARNING": f"{component}: High memory usage",
                "ERROR": f"{component}: Connection failed"
            }

            entry = f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {messages[level]}\n"
            log_entries.append(entry)

        return self._write_text(filepath, ''.join(sorted(log_entries)))

    def _generate_readme(self, filepath: str) -> bool:
        """Generate project documentation"""

        content = f"""FTP Test Data Documentation
===========================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Files included:
- employee_records.csv: Employee data
- app_config.json: App configuration  
- sales_data.csv: Sales transactions
- system.log: System logs
- network_config.ini: Network settings

Usage:
1. Upload files to FTP server
2. Test download functionality
3. Verify file integrity
4. Clean up after testing

Note: All data is fictional for testing only.
"""
        return self._write_text(filepath, content)

    def _generate_network_config(self, filepath: str) -> bool:
        """Generate network configuration INI"""
        content = """[NETWORK]
interface=eth0
ip_address=192.168.1.100
gateway=192.168.1.1
dns=8.8.8.8

[FTP]
port=21
passive_mode=true
max_connections=50
timeout=300

[SECURITY]
firewall_enabled=true
anonymous_access=false
max_attempts=3
"""
        return self._write_text(filepath, content)

    def generate_file(self, generator: FileGenerator) -> bool:
        """Generate a single file"""

        filepath = os.path.join(self.output_dir, generator.filename)
        if generator.generator_func(filepath):
            size = os.path.getsize(filepath)
            size_str = f"{size} bytes" if size < 1024 else f"{size/1024:.1f} KB"
            print(f"✅ {generator.name}: {generator.filename} ({size_str})")
            return True
        else:
            print(f"❌ Failed: {generator.name}")
            return False

    def generate_all(self) -> None:
        """Generate all test files"""

        print("FTP Test Data Generator")
        print("=" * 40)

        if not self.create_output_directory():
            print("Failed to create output directory")
            return

        print(f"Generating files in: {self.output_dir}")
        print("-" * 40)

        for generator in self.generators:
            if self.generate_file(generator):
                self.success_count += 1

        self.print_summary()

    def print_summary(self) -> None:
        """Print generation summary"""

        total_files = len(self.generators)
        print(f"\nSummary: {self.success_count}/{total_files} files created")

        if self.success_count == total_files:
            print("🎉 All files generated successfully!")
        else:
            print(f"⚠️  {total_files - self.success_count} files failed")


def main():
    """Main entry point"""

    parser = argparse.ArgumentParser(description='Generate FTP test data')
    parser.add_argument('--dir', default='ftp_test_data',
                        help='Output directory (default: ftp_test_data)')
    args = parser.parse_args()

    generator = FTPTestDataGenerator(args.dir)
    generator.generate_all()


if __name__ == "__main__":
    main()
