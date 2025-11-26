import html
from typing import Optional
from ShriBots import dispatcher, LOGGER
from ShriBots.Handlers.validation import user_admin, user_not_admin, is_user_admin
from ShriBots.Database import reporting_sql as sql
from telegram import Chat, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update, User
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import mention_html

@user_admin
def report_setting(update: Update, context: CallbackContext):
    args = context.args
    chat = update.effective_chat
    msg = update.effective_message

    if chat.type == chat.PRIVATE:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_user_setting(chat.id, True)
                msg.reply_text("Turned on reporting!")
            elif args[0] in ("no", "off"):
                sql.set_user_setting(chat.id, False)
                msg.reply_text("Turned off reporting!")
        else:
            msg.reply_text(f"Your report preference: `{sql.user_should_report(chat.id)}`")
    else:
        if len(args) >= 1:
            if args[0] in ("yes", "on"):
                sql.set_chat_setting(chat.id, True)
                msg.reply_text("Reporting enabled for this group!")
            elif args[0] in ("no", "off"):
                sql.set_chat_setting(chat.id, False)
                msg.reply_text("Reporting disabled for this group!")
        else:
            msg.reply_text(f"Group report setting: `{sql.chat_should_report(chat.id)}`")

@user_not_admin
def report(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    if chat and message.reply_to_message and sql.chat_should_report(chat.id):
        reported_user = message.reply_to_message.from_user
        admin_list = chat.get_administrators()
        
        if user.id == reported_user.id:
            message.reply_text("You can't report yourself!")
            return
            
        msg = f"Report from {html.escape(chat.title)}\nReported by: {mention_html(user.id, user.first_name)}\nReported user: {mention_html(reported_user.id, reported_user.first_name)}"
        
        for admin in admin_list:
            if admin.user.is_bot:
                continue
            if sql.user_should_report(admin.user.id):
                try:
                    context.bot.send_message(admin.user.id, msg, parse_mode=ParseMode.HTML)
                except Unauthorized:
                    pass
        
        message.reply_text("Report sent to admins!")
        return msg

__help__ = """
• /report <reason> - Report a message to admins
• @admin - Report a message to admins
• /reports <on/off> - Enable/disable reporting
"""

__mod_name__ = "Reporting"

SETTING_HANDLER = CommandHandler("reports", report_setting, run_async=True)
REPORT_HANDLER = CommandHandler("report", report, filters=Filters.chat_type.groups, run_async=True)
ADMIN_REPORT_HANDLER = MessageHandler(Filters.regex(r"(?i)@admin(s)?"), report, run_async=True)

dispatcher.add_handler(SETTING_HANDLER)
dispatcher.add_handler(REPORT_HANDLER)
dispatcher.add_handler(ADMIN_REPORT_HANDLER)
