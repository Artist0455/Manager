from ShriBots import dispatcher
from ShriBots.Handlers.validation import user_admin
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler
from telegram.utils.helpers import mention_html

@user_admin
def promote(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot

    if not message.reply_to_message:
        message.reply_text("Reply to a user to promote them!")
        return

    user = message.reply_to_message.from_user
    member = chat.get_member(user.id)

    if member.status in ["administrator", "creator"]:
        message.reply_text("This user is already an admin!")
        return

    try:
        bot.promote_chat_member(
            chat.id,
            user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
        )
        message.reply_text(
            f"Promoted {mention_html(user.id, user.first_name)} to Admin!",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        message.reply_text(f"Failed to promote: {str(e)}")

@user_admin
def demote(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot

    if not message.reply_to_message:
        message.reply_text("Reply to a user to demote them!")
        return

    user = message.reply_to_message.from_user
    member = chat.get_member(user.id)

    if member.status not in ["administrator", "creator"]:
        message.reply_text("This user is not an admin!")
        return

    if member.status == "creator":
        message.reply_text("Can't demote chat creator!")
        return

    try:
        bot.promote_chat_member(
            chat.id,
            user.id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
        )
        message.reply_text(
            f"Demoted {mention_html(user.id, user.first_name)}!",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        message.reply_text(f"Failed to demote: {str(e)}")

@user_admin
def adminlist(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat

    admin_list = []
    for admin in chat.get_administrators():
        if admin.user.is_bot:
            continue
        name = admin.user.first_name
        if admin.user.username:
            name = f"@{admin.user.username}"
        admin_list.append(f"• {name}")

    if admin_list:
        text = "👑 Admins:\n" + "\n".join(admin_list)
    else:
        text = "No admins found!"

    message.reply_text(text)

__help__ = """
**Admin Management:**
• /promote - Promote a user to admin (reply to user)
• /demote - Demote an admin (reply to user)  
• /adminlist - List all admins in chat
"""

__mod_name__ = "Admins"

PROMOTE_HANDLER = CommandHandler("promote", promote, run_async=True)
DEMOTE_HANDLER = CommandHandler("demote", demote, run_async=True)
ADMINLIST_HANDLER = CommandHandler("adminlist", adminlist, run_async=True)

dispatcher.add_handler(PROMOTE_HANDLER)
dispatcher.add_handler(DEMOTE_HANDLER)
dispatcher.add_handler(ADMINLIST_HANDLER)
