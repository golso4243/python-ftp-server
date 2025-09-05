#!/usr/bin/env python3
"""
FTP Server for Cybersecurity Lab
Built with pyftpdlib for educational purposes to observe unencrypted transfers in Wireshark
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
    """Custom FTP handler with enhanced logging for cybersecurity analysis"""
    
    def on_connect(self):
        """Log client connections"""
        logging.info(f"[CONNECTION] Client connected from {self.remote_ip}:{self.remote_port}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CLIENT CONNECTED: {self.remote_ip}:{self.remote_port}")

    def on_disconnect(self):
        """Log client disconnections"""
        logging.info(f"[DISCONNECTION] Client {self.remote_ip}:{self.remote_port} disconnected")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] CLIENT DISCONNECTED: {self.remote_ip}:{self.remote_port}")

    def on_login(self, username):
        """Log successful logins"""
        logging.info(f"[LOGIN] User '{username}' logged in from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGIN SUCCESS: User '{username}' from {self.remote_ip}")

    def on_login_failed(self, username, password):
        """Log failed login attempts"""
        logging.warning(f"[LOGIN FAILED] Failed login attempt - Username: '{username}', Password: '{password}' from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGIN FAILED: User '{username}' from {self.remote_ip}")

    def on_logout(self, username):
        """Log user logouts"""
        logging.info(f"[LOGOUT] User '{username}' logged out from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] LOGOUT: User '{username}' from {self.remote_ip}")

    def on_file_sent(self, file):
        """Log file downloads (sent to client)"""
        logging.info(f"[DOWNLOAD] File '{file}' downloaded by {self.username} from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FILE DOWNLOADED: '{file}' by {self.username}")

    def on_file_received(self, file):
        """Log file uploads (received from client)"""
        logging.info(f"[UPLOAD] File '{file}' uploaded by {self.username} from {self.remote_ip}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] FILE UPLOADED: '{file}' by {self.username}")

    def ftp_LIST(self, path):
        """Override LIST command to log directory listings"""
        logging.info(f"[COMMAND] LIST command executed by {self.username} for path: {path}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: LIST '{path}' by {self.username}")
        return super().ftp_LIST(path)

    def ftp_PWD(self, line):
        """Override PWD command to log current directory requests"""
        logging.info(f"[COMMAND] PWD command executed by {self.username}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: PWD by {self.username}")
        return super().ftp_PWD(line)

    def ftp_CWD(self, path):
        """Override CWD command to log directory changes"""
        logging.info(f"[COMMAND] CWD command executed by {self.username} to: {path}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COMMAND: CWD '{path}' by {self.username}")
        return super().ftp_CWD(path)

def setup_logging():
    """Configure logging for the FTP server"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_filename = os.path.join(log_dir, f"ftp_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    return log_filename

def create_server_directory(server_root):
    """Create the FTP server root directory if it doesn't exist"""
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
    """Main function to start the FTP server"""
    # Load environment variables
    load_dotenv('.env.development')
    
    # Setup logging
    log_file = setup_logging()
    
    # Get configuration from environment variables
    FTP_USER = os.getenv('FTP_USER', 'labuser')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD', 'labpass123')
    FTP_HOST = os.getenv('FTP_HOST', '127.0.0.1')
    FTP_PORT = int(os.getenv('FTP_PORT', '2121'))
    FTP_SERVER_ROOT = os.getenv('FTP_SERVER_ROOT', 'ftp_server_root')
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
    
    # Create server directory
    server_root_path = create_server_directory(FTP_SERVER_ROOT)
    
    # Create authorizer with dummy user
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, server_root_path, perm=FTP_PERMISSIONS)
    
    # Allow anonymous access for testing (optional - comment out for security)
    # authorizer.add_anonymous(server_root_path, perm="elr")
    
    # Create FTP handler with custom logging
    handler = CustomFTPHandler
    handler.authorizer = authorizer
    
    # Configure handler settings
    handler.banner = "FTP Server ready for cybersecurity analysis."
    handler.max_login_attempts = 3
    handler.permit_foreign_addresses = True  # Allow data connections from different IPs
    handler.passive_ports = range(60000, 65535)  # Passive port range for data connections
    
    # Create and configure FTP server
    try:
        server = FTPServer((FTP_HOST, FTP_PORT), handler)
        
        # Server settings
        server.max_cons = 256
        server.max_cons_per_ip = 5
        
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting FTP server...")
        print(f"Server listening on {FTP_HOST}:{FTP_PORT}")
        print("Press Ctrl+C to stop the server")
        print("\nWARNING: This server transmits data unencrypted for lab purposes!")
        print("Monitor traffic with Wireshark on port", FTP_PORT)
        print("-"*60)
        
        # Start the server
        server.serve_forever()
        
    except PermissionError:
        print(f"ERROR: Permission denied to bind to port {FTP_PORT}")
        print("Try running as administrator or use a port > 1024")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Cannot start server - {e}")
        print("Make sure the port is not already in use")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server shutdown requested...")
        server.close_all()
        print("FTP Server stopped.")

if __name__ == "__main__":
    main()
