import argparse
import os
import datetime
import json
from modules.ssh_connector import SSHConnector
from modules.diagnostics_linux import run_linux_diagnostics
from modules.report_generator import generate_html_report, generate_text_report
from modules.zip_packager import zip_output_dir

# Future feature modules (to be implemented)
from modules.db_checker import run_db_checks
from modules.diagnostics_windows import run_windows_diagnostics
from modules.keyword_filter import apply_keyword_filter
from modules.virtualization import detect_virtualization

def save_output(output, output_dir, filename):
    with open(os.path.join(output_dir, filename), 'w') as f:
        f.write(output)

def load_servers_from_file(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Remote Diagnostics and Log Collector")
    parser.add_argument('--target', help='Target server IP or hostname')
    parser.add_argument('--user', help='SSH username')
    parser.add_argument('--password', help='SSH password')
    parser.add_argument('--os', choices=['linux', 'windows'], help='Target OS')
    parser.add_argument('--filter', help='Comma-separated keywords to filter logs')
    parser.add_argument('--server-list', help='Path to JSON file with server definitions, including DB info, OS type, and virtualization settings')

    args = parser.parse_args()

    if args.server_list:
        servers = load_servers_from_file(args.server_list)
    else:
        if not all([args.target, args.user, args.password, args.os]):
            print("[!] Missing required arguments for single target mode.")
            return
        servers = [{
            "hostname": args.target,
            "username": args.user,
            "password": args.password,
            "os": args.os
        }]

    for srv in servers:
        hostname = srv['hostname']
        username = srv['username']
        password = srv['password']
        os_type = srv['os']

        print(f"[*] Connecting to {hostname}...")
        ssh = SSHConnector(hostname, username, password)

        if not ssh.connect():
            print(f"[!] SSH connection failed for {hostname}.")
            continue

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = f"output/diagnostics_{hostname}_{timestamp}"
        os.makedirs(output_dir, exist_ok=True)

        print(f"[*] Running diagnostics on {hostname}...")

        if os_type == 'linux':
            diagnostics = run_linux_diagnostics(ssh, args.filter)
            for key, value in diagnostics.items():
                save_output(value, output_dir, f"{key}.log")

            generate_text_report(diagnostics, output_dir, hostname)
            generate_html_report(diagnostics, output_dir, hostname)
            zip_path = zip_output_dir(output_dir)
            print(f"[✓] Diagnostics complete for {hostname}. ZIP: {zip_path}")

        elif os_type == 'windows':
            diagnostics = run_windows_diagnostics(ssh, args.filter)
            for key, value in diagnostics.items():
                save_output(value, output_dir, f"{key}.log")

            generate_text_report(diagnostics, output_dir, hostname)
            generate_html_report(diagnostics, output_dir, hostname)
            zip_path = zip_output_dir(output_dir)
            print(f"[✓] Diagnostics complete for {hostname}. ZIP: {zip_path}")

        ssh.disconnect()

if __name__ == '__main__':
    main()
