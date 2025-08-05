def run_linux_diagnostics(ssh, filter_keywords=None):
    diagnostics = {}

    commands = {
        "system_info": "uname -a && lsb_release -a || cat /etc/os-release",
        "uptime": "uptime",
        "cpu_memory": "top -b -n1 | head -20",
        "disk_usage": "df -h",
        "network_info": "ip a && netstat -tulnp",
        "routes": "ip route",
        "firewall": "sudo iptables -L || sudo ufw status",
        "processes": "ps aux --sort=-%mem | head -10",
        "dmesg": "dmesg | tail -n 100",
        "syslog": "cat /var/log/syslog || cat /var/log/messages",
        "auth_log": "cat /var/log/auth.log"
    }

    for name, cmd in commands.items():
        output = ssh.run_command(cmd)
        if filter_keywords:
            filtered = []
            keywords = [k.strip().lower() for k in filter_keywords.split(",")]
            for line in output.splitlines():
                if any(k in line.lower() for k in keywords):
                    filtered.append(line)
            output = '\n'.join(filtered)
        diagnostics[name] = output

    return diagnostics
