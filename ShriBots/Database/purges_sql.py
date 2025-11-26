import threading
from sqlalchemy import Column, String, Integer
from ShriBots import BASE, SESSION

class PurgeFrom(BASE):
    __tablename__ = "purge_from"
    chat_id = Column(String(14), primary_key=True)
    message_from = Column(Integer)

    def __init__(self, chat_id, message_from):
        self.chat_id = chat_id
        self.message_from = message_from

PurgeFrom.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def purgefrom(chat_id, message_from):
    with INSERTION_LOCK:
        prev = SESSION.query(PurgeFrom).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        purge_f = PurgeFrom(str(chat_id), message_from)
        SESSION.add(purge_f)
        SESSION.commit()

def is_purgefrom(chat_id, message_from):
    try:
        return SESSION.query(PurgeFrom).get((str(chat_id), message_from))
    finally:
        SESSION.close()

def show_purgefrom(chat_id):
    try:
        return SESSION.query(PurgeFrom).filter(PurgeFrom.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()

def clear_purgefrom(chat_id, message_from):
    with INSERTION_LOCK:
        if prev := SESSION.query(PurgeFrom).get((str(chat_id), message_from)):
            SESSION.delete(prev)
            SESSION.commit()
            return True
        SESSION.close()
        return False
