#!/usr/bin/env python3
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests

from common.ssh_utils import get_client, run_command
from common.mail_utils import send_mail
from config.config import SERVERS, ALCASAR

def alcasar_login():
    session = requests.Session()

    page = session.get(f"{ALCASAR['portal_url']}/intercept.php", verify=False, timeout=15).text

    challenge_match = re.search(r'name="challenge" value="([^"]+)"', page)
    userurl_match = re.search(r'name="userurl" value="([^"]+)"', page)
    if not challenge_match or not userurl_match:
        raise RuntimeError("Impossible de récupérer challenge/userurl depuis intercept.php")

    resp = session.post(
        f"{ALCASAR['portal_url']}/intercept.php",
        data={
            "challenge": challenge_match.group(1),
            "userurl": userurl_match.group(1),
            "username": ALCASAR["user"],
            "password": ALCASAR["password"],
            "button": "Authentication",
        },
        verify=False,
        timeout=15,
    )
    resp.raise_for_status()
    return session

def alcasar_logout(session):
    try:
        session.get(f"{ALCASAR['portal_url']}/deconnexion.php", verify=False, timeout=15)
    except requests.RequestException as exc:
        print(f"Avertissement : échec de la déconnexion Alcasar ({exc})", file=sys.stderr)

def update_server(server):
    client = get_client(server)
    try:
        sudo_password = SERVERS[server].get("sudo_password")
        run_command(client, "apt-get update -y", sudo=True, sudo_password=sudo_password)
        run_command(client, "apt-get upgrade -y", sudo=True, sudo_password=sudo_password)
        out, _, _ = run_command(
            client, "test -f /var/run/reboot-required && echo REBOOT_NEEDED || echo OK"
        )
    finally:
        client.close()
    return "REBOOT_NEEDED" in out

def main():
    session = alcasar_login()
    print("Connecté au portail Alcasar.")
    try:
        reboot_needed = []
        for server in SERVERS:
            print(f"Mise à jour de {server}...")
            if update_server(server):
                reboot_needed.append(server)

        if reboot_needed:
            send_mail(
                "[PSMM] Redémarrage requis après mise à jour",
                "Les serveurs suivants nécessitent un redémarrage :\n" + "\n".join(reboot_needed),
            )
            print("Mail d'alerte redémarrage envoyé.")
        else:
            print("Aucun redémarrage requis.")
    finally:
        alcasar_logout(session)
        print("Déconnecté du portail Alcasar.")

if __name__ == "__main__":
    main()
