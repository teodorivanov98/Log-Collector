
# modules/db_checker.py
import re

def run_db_checks(ssh, db_info):
    results = {}
    db_type = db_info.get("type")
    db_user = db_info.get("user")
    db_pass = db_info.get("password")
    db_name = db_info.get("database")

    if db_type == "postgresql":
        cmd = f"PGPASSWORD={db_pass} psql -U {db_user} -d {db_name} -c 'SELECT version();'"
        status, output = ssh.execute_command(cmd)
        results['postgresql_version'] = output if status else "PostgreSQL check failed"

    elif db_type == "mysql":
        cmd = f"mysql -u {db_user} -p{db_pass} -e 'SELECT VERSION();'"
        status, output = ssh.execute_command(cmd)
        results['mysql_version'] = output if status else "MySQL check failed"

    elif db_type == "oracle":
        # Assuming Oracle SQL*Plus is configured with environment variables
        cmd = f"echo 'SELECT * FROM v$version;' | sqlplus -S {db_user}/{db_pass}@{db_name}"
        status, output = ssh.execute_command(cmd)
        results['oracle_version'] = output if status else "Oracle DB check failed"

    else:
        results['db_error'] = f"Unsupported DB type: {db_type}"

    return results