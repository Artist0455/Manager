import re
from ShriBots import dispatcher
from ShriBots.Handlers.validation import user_admin
from ShriBots.Database import filters_sql as sql
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters

@user_admin
def add_filter(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    args = msg.text.split(None, 1)

    if len(args) < 2:
        msg.reply_text("Usage: /filter <keyword> <reply message>")
        return

    keyword = args[1]
    
    if msg.reply_to_message:
        if msg.reply_to_message.text:
            text = msg.reply_to_message.text
        elif msg.reply_to_message.caption:
            text = msg.reply_to_message.caption
        else:
            text = ""
    else:
        msg.reply_text("Please reply to a message to set filter for.")
        return

    sql.add_filter(chat.id, keyword, text)
    msg.reply_text(f"Added filter for '{keyword}'!")

@user_admin
def stop_filter(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    args = msg.text.split(None, 1)

    if len(args) < 2:
        msg.reply_text("Usage: /stop <keyword>")
        return

    keyword = args[1]
    sql.remove_filter(chat.id, keyword)
    msg.reply_text(f"Removed filter '{keyword}'!")

def list_filters(update: Update, context: CallbackContext):
    chat = update.effective_chat
    all_filters = sql.get_chat_filters(chat.id)

    if not all_filters:
        update.effective_message.reply_text("No filters active here!")
        return

    filter_list = "Active filters:\n"
    for keyword in all_filters:
        filter_list += f"• {keyword}\n"

    update.effective_message.reply_text(filter_list)

def reply_filter(update: Update, context: CallbackContext):
    chat = update.effective_chat
    message = update.effective_message
    text = message.text or message.caption

    if not text:
        return

    all_filters = sql.get_chat_filters(chat.id)
    for keyword in all_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_reply = sql.get_filter(chat.id, keyword)
            message.reply_text(filter_reply)
            break

__help__ = """
**Filters Commands:**
• /filter <keyword> <reply> - Add a filter
• /stop <keyword> - Remove a filter  
• /filters - List all filters

When someone says the keyword, bot will reply with the set message.
"""

__mod_name__ = "Filters"

ADD_FILTER_HANDLER = CommandHandler("filter", add_filter, run_async=True)
STOP_FILTER_HANDLER = CommandHandler("stop", stop_filter, run_async=True)
LIST_FILTERS_HANDLER = CommandHandler("filters", list_filters, run_async=True)
FILTER_MSG_HANDLER = MessageHandler(Filters.text & Filters.chat_type.groups, reply_filter, run_async=True)

dispatcher.add_handler(ADD_FILTER_HANDLER)
dispatcher.add_handler(STOP_FILTER_HANDLER)
dispatcher.add_handler(LIST_FILTERS_HANDLER)
dispatcher.add_handler(FILTER_MSG_HANDLER)
