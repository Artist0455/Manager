from ShriBots import dispatcher
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

def info(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        if len(context.args) >= 1:
            user_id = context.args[0]
            try:
                user = context.bot.get_chat(user_id)
            except:
                message.reply_text("User not found!")
                return
        else:
            user = update.effective_user

    text = (
        f"User Info:\n"
        f"• ID: <code>{user.id}</code>\n"
        f"• First Name: {user.first_name}\n"
        f"• Username: @{user.username if user.username else 'N/A'}\n"
        f"• Profile: {mention_html(user.id, 'Link')}"
    )
    
    message.reply_text(text, parse_mode=ParseMode.HTML)

def id(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if message.reply_to_message:
        user = message.reply_to_message.from_user
        text = (
            f"Your ID: <code>{user.id}</code>\n"
            f"Chat ID: <code>{chat.id}</code>\n"
            f"Replied User ID: <code>{user.id}</code>"
        )
    else:
        text = (
            f"Your ID: <code>{user.id}</code>\n"
            f"Chat ID: <code>{chat.id}</code>"
        )
    
    message.reply_text(text, parse_mode=ParseMode.HTML)

def whois(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    
    if not message.reply_to_message:
        message.reply_text("Please reply to a user to get their info!")
        return
        
    user = message.reply_to_message.from_user
    member = chat.get_member(user.id)
    
    text = (
        f"👤 User Details:\n"
        f"• Name: {user.first_name} {user.last_name or ''}\n"
        f"• Username: @{user.username or 'N/A'}\n"
        f"• ID: <code>{user.id}</code>\n"
        f"• Status: {member.status}\n"
        f"• Is Bot: {user.is_bot}\n"
        f"• Language: {user.language_code or 'N/A'}"
    )
    
    message.reply_text(text, parse_mode=ParseMode.HTML)

__help__ = """
**User Info Commands:**
• /info - Get your info
• /info @username - Get user info
• /id - Get your ID and chat ID  
• /whois - Detailed user info (reply to user)
"""

__mod_name__ = "Info"

INFO_HANDLER = CommandHandler("info", info, run_async=True)
ID_HANDLER = CommandHandler("id", id, run_async=True)
WHOIS_HANDLER = CommandHandler("whois", whois, run_async=True)

dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(WHOIS_HANDLER)
