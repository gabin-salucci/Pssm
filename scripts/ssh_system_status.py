#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.ssh_utils import get_client, run_command
from common.db_utils import get_connection
from config.config import SERVERS

CPU_CMD = "export LC_ALL=C; vmstat 1 2 | tail -1 | awk '{print 100-$15}'"
RAM_CMD = "export LC_ALL=C; free | awk '/Mem:/{printf \"%.1f\", $3/$2*100}'"
DISK_CMD = "df / | awk 'NR==2{print $5}' | tr -d '%'"

def collect(server):
    client = get_client(server)
    try:
        cpu, _, _ = run_command(client, CPU_CMD)
        ram, _, _ = run_command(client, RAM_CMD)
        disk, _, _ = run_command(client, DISK_CMD)
    finally:
        client.close()
    return float(cpu.strip() or 0), float(ram.strip() or 0), float(disk.strip() or 0)

def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for server in SERVERS:
                cpu, ram, disk = collect(server)
                cur.execute(
                    """
                    INSERT INTO system_status (server, cpu_pct, ram_pct, disk_pct)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (server, cpu, ram, disk),
                )
                print(f"{server}: CPU={cpu}% RAM={ram}% DISK={disk}%")

            cur.execute("DELETE FROM system_status WHERE recorded_at < NOW() - INTERVAL 72 HOUR")
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
