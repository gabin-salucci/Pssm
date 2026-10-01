#!/usr/bin/env python3
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

from common.db_utils import get_connection
from common.mail_utils import send_mail
from config.config import SERVERS, THRESHOLDS
from ssh_system_status import collect

MAIL_TYPE = "system_alert"

def already_sent_recently(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT sent_at FROM mail_log WHERE mail_type=%s ORDER BY sent_at DESC LIMIT 1",
            (MAIL_TYPE,),
        )
        row = cur.fetchone()
    if not row:
        return False
    return (datetime.now() - row["sent_at"]) < timedelta(hours=1)

def log_mail_sent(conn):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO mail_log (mail_type, sent_at) VALUES (%s, NOW())", (MAIL_TYPE,))
    conn.commit()

def main():
    alerts = []
    for server in SERVERS:
        cpu, ram, disk = collect(server)
        if cpu > THRESHOLDS["cpu"]:
            alerts.append(f"{server} : CPU {cpu}% (seuil {THRESHOLDS['cpu']}%)")
        if disk > THRESHOLDS["disk"]:
            alerts.append(f"{server} : DISK {disk}% (seuil {THRESHOLDS['disk']}%)")
        if ram > THRESHOLDS["ram"]:
            alerts.append(f"{server} : RAM {ram}% (seuil {THRESHOLDS['ram']}%)")

    if not alerts:
        print("Aucun dépassement de seuil.")
        return

    conn = get_connection()
    try:
        if already_sent_recently(conn):
            print("Dépassement détecté, mais mail déjà envoyé il y a moins d'une heure.")
            return

        body = "Alertes système détectées :\n\n" + "\n".join(alerts)
        send_mail("[PSMM] Alerte ressources système", body)
        log_mail_sent(conn)
        print("Mail d'alerte envoyé.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
