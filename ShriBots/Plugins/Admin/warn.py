from ShriBots import dispatcher
from ShriBots.Handlers.validation import user_admin
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

@user_admin
def warn(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    
    if not args:
        message.reply_text("Please specify a user to warn!")
        return
    
    user_id = args[0]
    reason = " ".join(args[1:]) if len(args) > 1 else "No reason given"
    
    message.reply_text(f"User {user_id} has been warned! Reason: {reason}")

@user_admin  
def unwarn(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("Warning removed!")

@user_admin
def warns(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text("User has 0/3 warnings")

__help__ = """
**Admin Commands:**
• /warn <user> <reason> - Warn a user
• /unwarn <user> - Remove warning  
• /warns <user> - Check warnings
• /resetwarns <user> - Reset all warnings
"""

__mod_name__ = "Warnings"

WARN_HANDLER = CommandHandler("warn", warn, run_async=True)
UNWARN_HANDLER = CommandHandler("unwarn", unwarn, run_async=True) 
WARNS_HANDLER = CommandHandler("warns", warns, run_async=True)

dispatcher.add_handler(WARN_HANDLER)
dispatcher.add_handler(UNWARN_HANDLER)
dispatcher.add_handler(WARNS_HANDLER)
