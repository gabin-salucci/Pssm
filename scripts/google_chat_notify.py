#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))

import requests

from config.config import GOOGLE_CHAT, SERVERS
from ssh_system_status import collect

def send_chat_message(text):
    resp = requests.post(GOOGLE_CHAT["webhook_url"], json={"text": text}, timeout=15)
    resp.raise_for_status()

def build_status_summary():
    lines = ["État des serveurs PSMM :"]
    for server in SERVERS:
        cpu, ram, disk = collect(server)
        lines.append(f"- {server} : CPU {cpu}% | RAM {ram}% | DISK {disk}%")
    return "\n".join(lines)

def main():
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        message = build_status_summary()

    send_chat_message(message)
    print("Message envoyé dans le Space Google Chat.")

if __name__ == "__main__":
    main()
