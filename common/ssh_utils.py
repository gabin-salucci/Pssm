import paramiko

from config.config import SERVERS

def get_client(server_key):
    if server_key not in SERVERS:
        raise ValueError(f"Serveur inconnu : {server_key!r}. Attendu : {list(SERVERS)}")
    s = SERVERS[server_key]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=s["host"],
        port=s.get("port", 22),
        username=s["monitor_user"],
        key_filename=s["key_path"],
        timeout=10,
    )
    return client

def run_command(client, command, sudo=False, sudo_password=None):
    real_command = f"sudo -S -p '' {command}" if sudo else command
    stdin, stdout, stderr = client.exec_command(real_command)

    if sudo and sudo_password:
        stdin.write(sudo_password + "\n")
        stdin.flush()

    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    code = stdout.channel.recv_exit_status()
    return out, err, code
