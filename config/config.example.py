SERVERS = {
    "ftp": {
        "host": "CHANGE_ME",
        "port": 22,
        "monitor_user": "monitor",
        "key_path": "/home/monitor/.ssh/id_ed25519_psmm",
        "sudo_password": "CHANGE_ME",
    },
    "web": {
        "host": "CHANGE_ME",
        "port": 22,
        "monitor_user": "monitor",
        "key_path": "/home/monitor/.ssh/id_ed25519_psmm",
        "sudo_password": "CHANGE_ME",
    },
    "mariadb": {
        "host": "CHANGE_ME",
        "port": 22,
        "monitor_user": "monitor",
        "key_path": "/home/monitor/.ssh/id_ed25519_psmm",
        "sudo_password": "CHANGE_ME",
    },
}

DB = {
    "host": "CHANGE_ME",
    "port": 3306,
    "user": "psmm_app",
    "password": "CHANGE_ME",
    "database": "psmm",
}

MAIL = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender": "votre.compte@gmail.com",
    "app_password": "CHANGE_ME",
    "admin_recipient": "admin-systeme@example.com",
}

THRESHOLDS = {
    "cpu": 70,
    "disk": 90,
    "ram": 80,
}

BACKUP = {
    "dir": "/home/monitor/psmm/backups",
    "keep": 7,
}

ALCASAR = {
    "portal_url": "https://alcasar.laplateforme.io",
    "user": "CHANGE_ME",
    "password": "CHANGE_ME",
}

GOOGLE_CHAT = {
    "webhook_url": "CHANGE_ME",
}
