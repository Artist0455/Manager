import threading
from sqlalchemy import Column, String, Text
from ShriBots import BASE, SESSION

class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(Text, primary_key=True)
    reply = Column(Text)

    def __init__(self, chat_id, keyword, reply):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply

Filters.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def add_filter(chat_id, keyword, reply):
    with INSERTION_LOCK:
        filt = Filters(str(chat_id), keyword, reply)
        SESSION.merge(filt)
        SESSION.commit()

def remove_filter(chat_id, keyword):
    with INSERTION_LOCK:
        filt = SESSION.query(Filters).get((str(chat_id), keyword))
        if filt:
            SESSION.delete(filt)
            SESSION.commit()

def get_filter(chat_id, keyword):
    try:
        return SESSION.query(Filters).get((str(chat_id), keyword))
    finally:
        SESSION.close()

def get_chat_filters(chat_id):
    try:
        return [x.keyword for x in SESSION.query(Filters).filter(Filters.chat_id == str(chat_id)).all()]
    finally:
        SESSION.close()

def num_filters():
    try:
        return SESSION.query(Filters).count()
    finally:
        SESSION.close()

def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        filts = SESSION.query(Filters).filter(Filters.chat_id == str(old_chat_id)).all()
        for filt in filts:
            filt.chat_id = str(new_chat_id)
        SESSION.commit()
