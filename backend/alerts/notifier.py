import requests
from config import Config

def send_discord_alert(threat):
    if not Config.DISCORD_WEBHOOK:
        return
    message = {
        "embeds": [{
            "title": f"🚨 {threat['type']} Detected!",
            "color": 15158332 if threat['severity'] == "CRITICAL" else 16776960,
            "fields": [
                {"name": "Severity", "value": threat['severity'], "inline": True},
                {"name": "Source IP", "value": threat['src_ip'], "inline": True},
                {"name": "Target IP", "value": threat['dst_ip'], "inline": True},
                {"name": "Details", "value": threat['details'], "inline": False},
            ]
        }]
    }
    try:
        requests.post(Config.DISCORD_WEBHOOK, json=message)
    except Exception as e:
        print(f"Discord alert error: {e}")

def notify(threat):
    send_discord_alert(threat)