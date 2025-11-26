import threading
from sqlalchemy import Column, String, Boolean
from ShriBots import BASE, SESSION

class ReportingSettings(BASE):
    __tablename__ = "reporting_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False)

    def __init__(self, chat_id, setting):
        self.chat_id = chat_id
        self.setting = setting

class UserReportingSettings(BASE):
    __tablename__ = "user_reporting_settings"
    user_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=False)

    def __init__(self, user_id, setting):
        self.user_id = user_id
        self.setting = setting

ReportingSettings.__table__.create(checkfirst=True)
UserReportingSettings.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

def chat_should_report(chat_id):
    try:
        setting = SESSION.query(ReportingSettings).get(str(chat_id))
        if setting:
            return setting.setting
        return False
    finally:
        SESSION.close()

def set_chat_setting(chat_id, setting):
    with INSERTION_LOCK:
        curr_setting = SESSION.query(ReportingSettings).get(str(chat_id))
        if not curr_setting:
            curr_setting = ReportingSettings(str(chat_id), setting)
        else:
            curr_setting.setting = setting
        SESSION.add(curr_setting)
        SESSION.commit()

def user_should_report(user_id):
    try:
        setting = SESSION.query(UserReportingSettings).get(str(user_id))
        if setting:
            return setting.setting
        return True
    finally:
        SESSION.close()

def set_user_setting(user_id, setting):
    with INSERTION_LOCK:
        curr_setting = SESSION.query(UserReportingSettings).get(str(user_id))
        if not curr_setting:
            curr_setting = UserReportingSettings(str(user_id), setting)
        else:
            curr_setting.setting = setting
        SESSION.add(curr_setting)
        SESSION.commit()

def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(ReportingSettings).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        SESSION.commit()
