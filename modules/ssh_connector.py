import paramiko

class SSHConnector:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=10
            )
            return True
        except Exception as e:
            print(f"[!] SSH connection error: {e}")
            return False

    def run_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode() + stderr.read().decode()
        except Exception as e:
            return f"Error executing command '{command}': {e}"

    def disconnect(self):
        if self.client:
            self.client.close()