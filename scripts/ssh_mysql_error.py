#!/usr/bin/env python3
import re
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.ssh_utils import get_client, run_command
from common.db_utils import get_connection
from config.config import SERVERS

PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2}).*"
    r"Access denied for user '([^']+)'@'([^']+)'"
)

def fetch_log_lines():
    client = get_client("mariadb")
    try:
        sudo_password = SERVERS["mariadb"].get("sudo_password")
        out, err, code = run_command(
            client,
            "journalctl -u mariadb --no-pager -o cat",
            sudo=True,
            sudo_password=sudo_password,
        )
        if code != 0:
            print("Erreur lors de la lecture du journal :", err, file=sys.stderr)
        return out.splitlines()
    finally:
        client.close()

def parse_timestamp(raw):
    raw = re.sub(r"\s+", " ", raw.strip())
    return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")

def main():
    lines = fetch_log_lines()
    inserted = 0

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for line in lines:
                match = PATTERN.match(line)
                if not match:
                    continue
                raw_ts, username, ip = match.groups()
                try:
                    attempt_time = parse_timestamp(raw_ts)
                except ValueError:
                    continue

                cur.execute(
                    """
                    INSERT IGNORE INTO auth_failures
                        (service, username, ip_address, attempt_time)
                    VALUES (%s, %s, %s, %s)
                    """,
                    ("mysql", username, ip, attempt_time),
                )
                inserted += cur.rowcount
        conn.commit()
    finally:
        conn.close()

    print(f"{inserted} nouvelle(s) tentative(s) échouée(s) MySQL enregistrée(s).")

if __name__ == "__main__":
    main()
