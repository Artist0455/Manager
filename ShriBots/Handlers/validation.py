from telegram import Chat, ChatMember, Update
from telegram.ext import CallbackContext

def is_user_admin(chat: Chat, user_id: int) -> bool:
    try:
        member = chat.get_member(user_id)
        return member.status in (ChatMember.ADMINISTRATOR, ChatMember.OWNER)
    except:
        return False

def user_admin(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        
        if user and is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        else:
            update.effective_message.reply_text("You need to be an admin to use this command.")
    return wrapper

def user_not_admin(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat
        
        if user and not is_user_admin(chat, user.id):
            return func(update, context, *args, **kwargs)
        else:
            update.effective_message.reply_text("This command is for users only.")
    return wrapper

def can_delete(chat: Chat, bot_id: int) -> bool:
    try:
        bot_member = chat.get_member(bot_id)
        return bot_member.can_delete_messages
    except:
        return False

def connection_status(func):
    def wrapper(update: Update, context: CallbackContext, *args, **kwargs):
        return func(update, context, *args, **kwargs)
    return wrapper
