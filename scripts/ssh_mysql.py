#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pymysql
from config.config import DB

def main():
    conn = pymysql.connect(
        host=DB["host"],
        port=DB.get("port", 3306),
        user=DB["user"],
        password=DB["password"],
        connect_timeout=10,
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES;")
            print("Connexion MariaDB réussie. Bases visibles :")
            for (db_name,) in cur.fetchall():
                print(" -", db_name)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
