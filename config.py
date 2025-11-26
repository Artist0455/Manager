import os

class Config:
    TOKEN = "8244179451:AAFPDc1nP5TMfPfLMHsOwzcC9NIS28NLYB0"
    API_ID = 25136703
    API_HASH = "accfaf5ecd981c67e481328515c39f89"
    OWNER_ID = 8385462088
    OWNER_USERNAME = "shribots"
    SUPPORT_CHAT = "shribots"
    EVENT_LOGS = -1003264890660
    JOIN_LOGGER = -1003264890660
    MESSAGE_DUMP = -1003264890660
    
    SQLALCHEMY_DATABASE_URI = "sqlite:///shribots.db"
    WORKERS = 8
    ALLOW_EXCL = True
    ALLOW_CHATS = True
    DEL_CMDS = True
    INFOPIC = False
    
    WEBHOOK = False
    PORT = 5000
    CERT_PATH = None
    
    LOAD = []
    NO_LOAD = ["translation"]
