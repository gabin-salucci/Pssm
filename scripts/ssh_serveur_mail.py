#!/usr/bin/env python3
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.db_utils import get_connection
from common.mail_utils import send_mail

def main():
    yesterday = date.today() - timedelta(days=1)

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT service, username, ip_address, attempt_time
                FROM auth_failures
                WHERE DATE(attempt_time) = %s
                ORDER BY attempt_time
                """,
                (yesterday,),
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        body = f"Aucune tentative de connexion échouée le {yesterday}."
    else:
        lines = [
            f"- [{r['service']}] {r['username']}@{r['ip_address']} le {r['attempt_time']}"
            for r in rows
        ]
        body = f"Tentatives de connexion échouées du {yesterday} ({len(rows)}) :\n\n" + "\n".join(lines)

    send_mail(f"[PSMM] Rapport des tentatives d'accès - {yesterday}", body)
    print("Mail envoyé.")

if __name__ == "__main__":
    main()
