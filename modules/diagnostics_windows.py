# modules/diagnostics_windows.py
def run_windows_diagnostics(ssh, keyword_filter=None):
    diagnostics = {}

    commands = {
        "system_info": "systeminfo",
        "ip_config": "ipconfig /all",
        "netstat": "netstat -ano",
        "services": "sc query state= all",
        "installed_programs": "wmic product get name,version",
        "disk_usage": "wmic logicaldisk get size,freespace,caption"
    }

    for key, cmd in commands.items():
        status, output = ssh.execute_command(cmd)
        diagnostics[key] = output if status else f"Failed to retrieve {key}"

    if keyword_filter:
        from modules.keyword_filter import apply_keyword_filter
        diagnostics = apply_keyword_filter(diagnostics, keyword_filter)

    return diagnostics