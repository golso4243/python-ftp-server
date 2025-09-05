#!/usr/bin/env python3
"""
FTP Server for Cybersecurity Lab
Built with pyftpdlib for educational purposes to observe unencrypted transfers in Wireshark

This server deliberately uses plain FTP (no TLS/SSL) to allow packet analysis
in cybersecurity training environments. Logs all commands and file transfers.
"""

import os
import sys
import logging
from datetime import datetime

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from dotenv import load_dotenv


class CustomFTPHandler(FTPHandler):
    """
    Custom FTP handler with enhanced logging for cybersecurity analysis

    Extends pyftpdlib's FTPHandler to log all client activities including
    connections, authentication attempts, file transfers, and commands.
    Provides real-time console output alongside file logging.
    """

    def on_connect(self):
        """Log client connections with IP and port information"""

        logging.info(
            f"[CONNECTION] Client connected from {self.remote_ip}:{self.remote_port}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CLIENT CONNECTED: {self.remote_ip}:{self.remote_port}")

    def on_disconnect(self):
        """Log client disconnections for session tracking"""

        logging.info(
            f"[DISCONNECTION] Client {self.remote_ip}:{self.remote_port} disconnected")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CLIENT DISCONNECTED: {self.remote_ip}:{self.remote_port}")

    def on_login(self, username):
        """Log successful authentication events"""

        logging.info(
            f"[LOGIN] User '{username}' logged in from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGIN SUCCESS: User '{username}' from {self.remote_ip}")

    def on_login_failed(self, username, password):
        """
        Log failed login attempts with credentials

        WARNING: Logs plaintext passwords for educational analysis
        Never do this in production environments
        """

        logging.warning(
            f"[LOGIN FAILED] Failed login attempt - Username: '{username}', Password: '{password}' from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGIN FAILED: User '{username}' from {self.remote_ip}")

    def on_logout(self, username):
        """Log user logout events for session completion tracking"""

        logging.info(
            f"[LOGOUT] User '{username}' logged out from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGOUT: User '{username}' from {self.remote_ip}")

    def on_file_sent(self, file):
        """Log file downloads (server -> client transfers)"""

        logging.info(
            f"[DOWNLOAD] File '{file}' downloaded by {self.username} from {self.remote_ip}")
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FILE DOWNLOADED: '{file}' by {self.username}")

    def on_file_received(self, file):
        """Log file uploads (client -> server transfers)"""

        logging.info(
            f"[UPLOAD] File '{file}' uploaded by {self.username} from {self.remote_ip}")
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FILE UPLOADED: '{file}' by {self.username}")

    def ftp_LIST(self, path):
        """Override LIST command to log directory listings"""

        logging.info(
            f"[COMMAND] LIST command executed by {self.username} for path: {path}")
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: LIST '{path}' by {self.username}")
        return super().ftp_LIST(path)

    def ftp_PWD(self, line):
        """Override PWD command to log current directory requests"""

        logging.info(f"[COMMAND] PWD command executed by {self.username}")
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: PWD by {self.username}")
        return super().ftp_PWD(line)

    def ftp_CWD(self, path):
        """Override CWD command to log directory changes"""

        logging.info(
            f"[COMMAND] CWD command executed by {self.username} to: {path}")
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: CWD '{path}' by {self.username}")
        return super().ftp_CWD(path)


def setup_logging():
    """
    Configure dual logging to file and console with timestamped log files.

    Creates logs directory if needed and generates unique log filename
    based on server start time for session tracking.

    Returns:
        str: Path to created log file
    """

    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Timestamp-based log filename for session identification
    log_filename = os.path.join(
        log_dir, f"ftp_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    return log_filename


def create_server_directory(server_root):
    """
    Initialize FTP server root directory with test structure.

    Creates directory hierarchy and sample files for lab exercises
    if server root doesn't exist.

    Args:
        server_root: Path to FTP server root directory

    Returns:
        str: Absolute path to server root directory
    """

    if not os.path.exists(server_root):
        os.makedirs(server_root)
        print(f"Created FTP server directory: {server_root}")

        # Create a sample subdirectory structure for testing
        sample_dirs = ["uploads", "downloads", "shared"]
        for dir_name in sample_dirs:
            dir_path = os.path.join(server_root, dir_name)
            os.makedirs(dir_path, exist_ok=True)

        # Create a sample file for testing downloads
        sample_file = os.path.join(server_root, "welcome.txt")
        with open(sample_file, 'w') as f:
            f.write("Welcome to the FTP Server!\n")
            f.write("This is a test file for cybersecurity lab purposes.\n")
            f.write(f"Server started at: {datetime.now()}\n")

    return os.path.abspath(server_root)


def main():
    """
    Main function to configure and start the FTP server.

    Loads environment configuration, sets up logging, creates server directory,
    configures authentication and handlers, then starts the server with
    appropriate error handling.
    """

    # Load environment variables
    load_dotenv('.env.development')

    # Initialize logging system
    log_file = setup_logging()

    # Load configuration from environment with lab-appropriate defaults
    FTP_USER = os.getenv('FTP_USER', 'labuser')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD', 'labpass123')
    FTP_HOST = os.getenv('FTP_HOST', '127.0.0.1')
    # Non-standard port for lab isolation
    FTP_PORT = int(os.getenv('FTP_PORT', '2121'))
    FTP_SERVER_ROOT = os.getenv('FTP_SERVER_ROOT', 'ftp_server_root')
    # Permission string: e=change dir, l=list, r=read, a=append, d=delete, f=rename, m=mkdir, w=write, M=chmod, T=time
    FTP_PERMISSIONS = os.getenv('FTP_PERMISSIONS', 'elradfmwMT')

    print("="*60)
    print("           FTP SERVER - CYBERSECURITY LAB")
    print("="*60)
    print(f"Server Host: {FTP_HOST}")
    print(f"Server Port: {FTP_PORT}")
    print(f"Username: {FTP_USER}")
    print(f"Password: {FTP_PASSWORD}")
    print(f"Server Root: {FTP_SERVER_ROOT}")
    print(f"Permissions: {FTP_PERMISSIONS}")
    print(f"Log File: {log_file}")
    print("="*60)

    # Initialize server directory structure
    server_root_path = create_server_directory(FTP_SERVER_ROOT)

    # Configure user authentication with single test account
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD,
                        server_root_path, perm=FTP_PERMISSIONS)

    # Anonymous access option (disabled by default for security)
    # Uncomment next line to allow anonymous connections for testing
    # authorizer.add_anonymous(server_root_path, perm="elr")

    # Configure FTP handler with custom logging capabilities
    handler = CustomFTPHandler
    handler.authorizer = authorizer

    # Configure handler security and connection settings
    handler.banner = "FTP Server ready for cybersecurity analysis."
    handler.max_login_attempts = 3  # Prevent brute force attacks
    # Allow data connections from different IPs (for NAT scenarios)
    handler.permit_foreign_addresses = True
    # High port range for passive data connections
    handler.passive_ports = range(60000, 65535)

    # Create and configure FTP server instance
    try:
        server = FTPServer((FTP_HOST, FTP_PORT), handler)

        # Server connection limits for resource management
        server.max_cons = 256  # Maximum concurrent connections
        server.max_cons_per_ip = 5  # Per-IP connection limit to prevent abuse

        print(
            f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting FTP server...")
        print(f"Server listening on {FTP_HOST}:{FTP_PORT}")
        print("Press Ctrl+C to stop the server")
        print("\nWARNING: This server transmits data unencrypted for lab purposes!")
        print("Monitor traffic with Wireshark on port", FTP_PORT)
        print("-"*60)

        # Start the server (blocks until interrupted)
        server.serve_forever()

    except PermissionError:
        # Common issue when trying to bind to privileged ports (<1024)
        print(f"ERROR: Permission denied to bind to port {FTP_PORT}")
        print("Try running as administrator or use a port > 1024")
        sys.exit(1)
    except OSError as e:
        # Handle port already in use or other socket errors
        print(f"ERROR: Cannot start server - {e}")
        print("Make sure the port is not already in use")
        sys.exit(1)
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C
        print(
            f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server shutdown requested...")
        server.close_all()  # Close all client connections
        print("FTP Server stopped.")


if __name__ == "__main__":
    main()
