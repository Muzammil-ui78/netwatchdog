class Config:
    MONGO_URI = "mongodb://localhost:27017/"
    DB_NAME = "netwatchdog"
    SECRET_KEY = "netwatchdog_secret_key"
    DEBUG = True
    NETWORK_INTERFACE = None

    PORT_SCAN_THRESHOLD = 10
    SYN_FLOOD_THRESHOLD = 100
    BRUTE_FORCE_THRESHOLD = 5

    ALERT_EMAIL = ""
    DISCORD_WEBHOOK = "https://discordapp.com/api/webhooks/1518660883939721298/pN3OfbCPjryKrFBHWiTzkAp-tNw_q1EtCzclK8P0guNYTWx0v3M3nd64i3CmWEQKAGhX"
