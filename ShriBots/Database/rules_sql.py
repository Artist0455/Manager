import threading
from sqlalchemy import Column, String, Integer
from ShriBots import BASE, SESSION

class Rules(BASE):
    __tablename__ = "rules"
    chat_id = Column(String(14), primary_key=True)
    rules = Column(String(2048))

    def __init__(self, chat_id, rules):
        self.chat_id = chat_id
        self.rules = rules

Rules.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def set_rules(chat_id, rules_text):
    with INSERTION_LOCK:
        rules = SESSION.query(Rules).get(str(chat_id))
        if not rules:
            rules = Rules(str(chat_id), rules_text)
        else:
            rules.rules = rules_text
        SESSION.add(rules)
        SESSION.commit()

def get_rules(chat_id):
    rules = SESSION.query(Rules).get(str(chat_id))
    ret = rules.rules if rules else ""
    SESSION.close()
    return ret

def num_chats():
    try:
        return SESSION.query(Rules).count()
    finally:
        SESSION.close()

def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Rules).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        SESSION.commit()
