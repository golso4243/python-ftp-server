#!/usr/bin/env python3
"""
FTP Client for Cybersecurity Lab
Built for educational purposes to test FTP server and observe unencrypted transfers
"""

import os
import sys
import cmd
import ftplib
import argparse
from datetime import datetime
from dotenv import load_dotenv


class FTPClient:
    """FTP Client class for connecting and performing operations"""

    def __init__(self, host='127.0.0.1', port=2121, username='labuser', password='labpass123'):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = None
        self.connected = False

    def connect(self):
        """Establish connection to FTP server"""

        try:
            print(f"Connecting to FTP server {self.host}:{self.port}...")
            self.ftp = ftplib.FTP()
            self.ftp.connect(self.host, self.port)

            print(f"Logging in as user: {self.username}")
            self.ftp.login(self.username, self.password)

            self.connected = True
            welcome_msg = self.ftp.getwelcome()
            print(f"Connected successfully!")
            print(f"Server message: {welcome_msg}")
            return True

        except ftplib.all_errors as e:
            print(f"Connection failed: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect from FTP server"""

        if self.ftp and self.connected:
            try:
                self.ftp.quit()
                print("Disconnected from FTP server.")
            except:
                pass  # Silent cleanup on connection errors
            finally:
                self.connected = False
                self.ftp = None

    def upload_file(self, local_path, remote_path=None):
        """Upload a file to the FTP server"""

        if not self.connected:
            print("Error: Not connected to FTP server")
            return False

        if not os.path.exists(local_path):
            print(f"Error: Local file '{local_path}' not found")
            return False

        # Default to basename if no remote path specified
        if remote_path is None:
            remote_path = os.path.basename(local_path)

        try:
            print(f"Uploading '{local_path}' to '{remote_path}'...")

            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_path}', file)

            print(f"Upload successful: {local_path} -> {remote_path}")
            return True

        except ftplib.all_errors as e:
            print(f"Upload failed: {e}")
            return False

    def download_file(self, remote_path, local_path=None):
        """Download a file from the FTP server"""

        if not self.connected:
            print("Error: Not connected to FTP server")
            return False

        # Default to basename in current directory if no local path specified
        if local_path is None:
            local_path = os.path.basename(remote_path)

        try:
            print(f"Downloading '{remote_path}' to '{local_path}'...")

            with open(local_path, 'wb') as file:
                self.ftp.retrbinary(f'RETR {remote_path}', file.write)

            print(f"Download successful: {remote_path} -> {local_path}")
            return True

        except ftplib.all_errors as e:
            print(f"Download failed: {e}")
            return False

    def list_files(self, path='.'):
        """List files in the specified directory"""
        if not self.connected:
            print("Error: Not connected to FTP server")
            return

        try:
            print(f"Directory listing for: {path}")
            print("-" * 40)

            files = []
            self.ftp.dir(path, files.append)  # Callback to collect output

            for file in files:
                print(file)

        except ftplib.all_errors as e:
            print(f"List failed: {e}")

    def get_current_directory(self):
        """Get current working directory"""

        if not self.connected:
            print("Error: Not connected to FTP server")
            return None

        try:
            pwd = self.ftp.pwd()
            return pwd
        except ftplib.all_errors as e:
            print(f"PWD failed: {e}")
            return None

    def change_directory(self, path):
        """Change current directory"""

        if not self.connected:
            print("Error: Not connected to FTP server")
            return False

        try:
            self.ftp.cwd(path)
            print(f"Changed directory to: {path}")
            return True
        except ftplib.all_errors as e:
            print(f"Change directory failed: {e}")
            return False


class FTPInteractiveShell(cmd.Cmd):
    """Interactive shell for FTP client commands"""

    intro = """
    ================================================================
                    FTP CLIENT - CYBERSECURITY LAB
    ================================================================
    Type 'help' or '?' to list commands.
    Type 'help <command>' for detailed help on a specific command.
    ================================================================
    """

    prompt = 'FTP> '

    def __init__(self):
        super().__init__()
        load_dotenv('.env')

        # Load configuration from environment
        self.host = os.getenv('FTP_HOST', '127.0.0.1')
        self.port = int(os.getenv('FTP_PORT', '2121'))
        self.username = os.getenv('FTP_USER', 'labuser')
        self.password = os.getenv('FTP_PASSWORD', 'labpass123')

        self.client = FTPClient(self.host, self.port,
                                self.username, self.password)

        # Auto-connect on startup and update prompt
        if self.client.connect():
            self.prompt = f'FTP({self.host})> '

    def do_connect(self, args):
        """Connect to FTP server: connect [host] [port] [username] [password]"""

        parts = args.split()

        # Override defaults with command line arguments
        if len(parts) >= 1:
            self.host = parts[0]
        if len(parts) >= 2:
            self.port = int(parts[1])
        if len(parts) >= 3:
            self.username = parts[2]
        if len(parts) >= 4:
            self.password = parts[3]

        self.client = FTPClient(self.host, self.port,
                                self.username, self.password)
        if self.client.connect():
            self.prompt = f'FTP({self.host})> '

    def do_disconnect(self, args):
        """Disconnect from FTP server"""

        self.client.disconnect()
        self.prompt = 'FTP> '

    def do_upload(self, args):
        """Upload a file: upload <local_file> [remote_file]"""

        parts = args.split()
        if len(parts) < 1:
            print("Usage: upload <local_file> [remote_file]")
            return

        local_file = parts[0]
        remote_file = parts[1] if len(parts) > 1 else None
        self.client.upload_file(local_file, remote_file)

    def do_download(self, args):
        """Download a file: download <remote_file> [local_file]"""

        parts = args.split()
        if len(parts) < 1:
            print("Usage: download <remote_file> [local_file]")
            return

        remote_file = parts[0]
        local_file = parts[1] if len(parts) > 1 else None
        self.client.download_file(remote_file, local_file)

    def do_ls(self, args):
        """List files: ls [directory]"""

        path = args.strip() or '.'
        self.client.list_files(path)

    def do_dir(self, args):
        """List files (alias for ls): dir [directory]"""

        self.do_ls(args)

    def do_pwd(self, args):
        """Show current directory: pwd"""

        current_dir = self.client.get_current_directory()
        if current_dir:
            print(f"Current directory: {current_dir}")

    def do_cd(self, args):
        """Change directory: cd <directory>"""

        if not args.strip():
            print("Usage: cd <directory>")
            return
        self.client.change_directory(args.strip())

    def do_stats(self, args):
        """Show connection statistics and server info"""

        if not self.client.connected:
            print("Not connected to server")
            return

        print(f"Connection Status: Connected")
        print(f"Server: {self.client.host}:{self.client.port}")
        print(f"Username: {self.client.username}")
        print(f"Current Directory: {self.client.get_current_directory()}")

        try:
            # Attempt to get server status via STAT command
            status = self.client.ftp.voidcmd('STAT')
            print(f"Server Status: {status}")
        except:
            print("Server Status: Not available")

    def do_status(self, args):
        """Show connection status (alias for stats)"""

        self.do_stats(args)

    def do_quit(self, args):
        """Quit the FTP client: quit"""

        print("Goodbye!")
        self.client.disconnect()
        return True

    def do_exit(self, args):
        """Exit the FTP client (alias for quit): exit"""

        return self.do_quit(args)

    def do_EOF(self, args):
        """Handle Ctrl+D"""

        print("\nGoodbye!")
        self.client.disconnect()
        return True

    def onecmd(self, line):
        """Override to handle errors gracefully"""

        try:
            return super().onecmd(line)
        except Exception as e:
            print(f"Error executing command: {e}")
            return False


def show_help():
    """Show help for command line usage"""

    help_text = """
FTP Client - Cybersecurity Lab

Usage:
    Interactive mode:
        python ftp_client.py
    
    Command mode:
        python ftp_client.py upload <local_file> [remote_file]
        python ftp_client.py download <remote_file> [local_file]
        python ftp_client.py ls [directory]
        python ftp_client.py connect [host] [port] [username] [password]

Examples:
    python ftp_client.py upload test.txt
    python ftp_client.py download welcome.txt
    python ftp_client.py upload ftp_test_data/app_config.json uploads/config.json
    python ftp_client.py ls uploads
    python ftp_client.py connect 192.168.1.100 2121 testuser testpass

Configuration:
    The client reads connection settings from .env.development file:
    - FTP_HOST (default: 127.0.0.1)
    - FTP_PORT (default: 2121)
    - FTP_USER (default: labuser)
    - FTP_PASSWORD (default: labpass123)
"""
    print(help_text)


def main():
    """Main function for command line argument processing"""
    if len(sys.argv) == 1:
        # Interactive mode
        shell = FTPInteractiveShell()
        try:
            shell.cmdloop()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            shell.client.disconnect()
    else:
        # Command line mode with arguments
        parser = argparse.ArgumentParser(
            description="FTP Client for Cybersecurity Lab")
        parser.add_argument(
            'command', help='Command to execute (upload, download, ls, connect)')
        parser.add_argument('args', nargs='*',
                            help='Arguments for the command')
        parser.add_argument('--host', default=None, help='FTP server host')
        parser.add_argument('--port', type=int,
                            default=None, help='FTP server port')
        parser.add_argument('--user', default=None, help='FTP username')
        parser.add_argument('--password', default=None, help='FTP password')

        # Handle help requests before parsing
        if '--help' in sys.argv or '-h' in sys.argv:
            show_help()
            return

        args = parser.parse_args()

        # Load environment variables
        load_dotenv('.env.development')

        # Command line args override environment variables
        host = args.host or os.getenv('FTP_HOST', '127.0.0.1')
        port = args.port or int(os.getenv('FTP_PORT', '2121'))
        username = args.user or os.getenv('FTP_USER', 'labuser')
        password = args.password or os.getenv('FTP_PASSWORD', 'labpass123')

        # Create client and connect
        client = FTPClient(host, port, username, password)

        try:
            if not client.connect():
                sys.exit(1)

            # Execute requested command
            command = args.command.lower()

            if command == 'upload':
                if len(args.args) < 1:
                    print("Usage: upload <local_file> [remote_file]")
                    sys.exit(1)
                local_file = args.args[0]
                remote_file = args.args[1] if len(args.args) > 1 else None
                success = client.upload_file(local_file, remote_file)
                sys.exit(0 if success else 1)

            elif command == 'download':
                if len(args.args) < 1:
                    print("Usage: download <remote_file> [local_file]")
                    sys.exit(1)
                remote_file = args.args[0]
                local_file = args.args[1] if len(args.args) > 1 else None
                success = client.download_file(remote_file, local_file)
                sys.exit(0 if success else 1)

            elif command == 'ls' or command == 'list':
                path = args.args[0] if len(args.args) > 0 else '.'
                client.list_files(path)

            elif command == 'connect':
                print("Already connected for command execution")

            else:
                print(f"Unknown command: {command}")
                show_help()
                sys.exit(1)

        finally:
            client.disconnect()


if __name__ == "__main__":
    main()
