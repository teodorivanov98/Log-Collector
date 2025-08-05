# modules/virtualization.py
def detect_virtualization(ssh):
    checks = [
        "lscpu | grep -i hypervisor",
        "systemd-detect-virt",
        "dmidecode -s system-product-name"
    ]

    result = {}
    for i, cmd in enumerate(checks, 1):
        status, output = ssh.execute_command(cmd)
        result[f"virt_check_{i}"] = output.strip() if status else f"Check {i} failed"

    return result
