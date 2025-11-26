from ShriBots import dispatcher
from ShriBots.Handlers.validation import user_admin, connection_status
from ShriBots.Database import rules_sql as sql
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import escape_markdown

@connection_status
def get_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    send_rules(update, chat_id)

def send_rules(update, chat_id, from_pm=False):
    bot = dispatcher.bot
    chat = bot.get_chat(chat_id)
    rules = sql.get_rules(chat_id)
    text = f"Rules for *{escape_markdown(chat.title)}*:\n\n{rules}"

    if from_pm and rules:
        update.effective_message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    elif from_pm:
        update.effective_message.reply_text("No rules set for this group yet!")
    elif rules:
        update.effective_message.reply_text(
            "Click below for rules:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Rules", url=f"t.me/{bot.username}?start={chat_id}")
            ]])
        )
    else:
        update.effective_message.reply_text("No rules set for this group yet!")

@connection_status
@user_admin
def set_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message

    if msg.reply_to_message:
        rules = msg.reply_to_message.text
    else:
        rules = msg.text.split(None, 1)[1] if len(msg.text.split()) > 1 else None

    if rules:
        sql.set_rules(chat_id, rules)
        msg.reply_text("Rules set successfully!")
    else:
        msg.reply_text("Please provide rules text!")

@connection_status
@user_admin
def clear_rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    sql.set_rules(chat_id, "")
    update.effective_message.reply_text("Rules cleared!")

__help__ = """
• /rules - Get group rules
• /setrules <rules> - Set group rules
• /clearrules - Clear group rules
"""

__mod_name__ = "Rules"

GET_RULES_HANDLER = CommandHandler("rules", get_rules, run_async=True)
SET_RULES_HANDLER = CommandHandler("setrules", set_rules, run_async=True)
CLEAR_RULES_HANDLER = CommandHandler("clearrules", clear_rules, run_async=True)

dispatcher.add_handler(GET_RULES_HANDLER)
dispatcher.add_handler(SET_RULES_HANDLER)
dispatcher.add_handler(CLEAR_RULES_HANDLER)
