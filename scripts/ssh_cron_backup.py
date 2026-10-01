#!/usr/bin/env python3
import glob
import os
import subprocess
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.config import DB, BACKUP

def main():
    os.makedirs(BACKUP["dir"], exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(BACKUP["dir"], f"psmm_backup_{timestamp}.sql")

    cmd = [
        "mysqldump",
        f"-h{DB['host']}",
        f"-P{DB.get('port', 3306)}",
        f"-u{DB['user']}",
        f"-p{DB['password']}",
        DB["database"],
    ]

    with open(filename, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)

    print(f"Sauvegarde créée : {filename}")

    backups = sorted(glob.glob(os.path.join(BACKUP["dir"], "psmm_backup_*.sql")))
    keep = BACKUP.get("keep", 7)
    for old in backups[:-keep] if len(backups) > keep else []:
        os.remove(old)
        print(f"Ancienne sauvegarde supprimée : {old}")

if __name__ == "__main__":
    main()
