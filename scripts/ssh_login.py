#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.ssh_utils import get_client, run_command

def main():
    server = sys.argv[1] if len(sys.argv) > 1 else "ftp"
    command = sys.argv[2] if len(sys.argv) > 2 else "df -h"

    client = get_client(server)
    try:
        out, err, code = run_command(client, command)
        print(f"--- {server} : '{command}' (code retour {code}) ---")
        print(out)
        if err:
            print("stderr :", err)
    finally:
        client.close()

if __name__ == "__main__":
    main()
