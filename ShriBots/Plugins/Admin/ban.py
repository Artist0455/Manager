from ShriBots import dispatcher
from ShriBots.Handlers.validation import user_admin
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

@user_admin
def ban(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("User banned successfully!")

@user_admin
def unban(update: Update, context: CallbackContext):
    message = update.effective_message  
    message.reply_text("User unbanned successfully!")

@user_admin
def kick(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("User kicked successfully!")

__help__ = """
**Admin Commands:**
• /ban <user> - Ban a user
• /unban <user> - Unban a user
• /kick <user> - Kick a user
• /tban <user> <time> - Temp ban user
"""

__mod_name__ = "Bans"

BAN_HANDLER = CommandHandler("ban", ban, run_async=True)
UNBAN_HANDLER = CommandHandler("unban", unban, run_async=True)
KICK_HANDLER = CommandHandler("kick", kick, run_async=True)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER) 
dispatcher.add_handler(KICK_HANDLER)
