# Fefes Bot
Ein kleiner Matrix-Bot, um den RSS-Feed von Fefes Blog in einen Matrix-Raum zu senden

![Beispielbild](https://raw.githubusercontent.com/UgnilJoZ/fefesbot/images/image.jpg)

## Dependencies
* python-matrix-nio
* python-beautifulsoup4
* python-requests
* python-feedparser

(Das sind jedenfalls die Pakete auf Arch Linux)

## Configuration
Einmal die `config.json.example` als `config.json` ins Bot-Arbeitsverzeichnis kopieren und mit echten Werten füllen (die Credentials kriegt man aus Element, wenn man sich einmal manuell als der Bot einloggt). Diese Datei unbedingt vor Lesezugriff durch andere schützen, denn das `access_token` ist da drin. Jeder Aufruf des Scripts holt die neuesten Nachrichten ab und postet sie in den Raum. Die ID der letzten Nachricht wird in der Datei `latest_post` gespeichert.

## Example systemd units
```ini
[Unit]
Description=Fefes-Blog-Bot

[Service]
User=fefesbot
Group=fefesbot
WorkingDirectory=/home/fefesbot
ExecStart=/usr/bin/python3 /opt/fefesbot/bot.py
```

```ini
[Unit]
Description=Timer für Fefes Blog

[Timer]
OnCalendar=minutely

[Install]
WantedBy=multi-user.target
```