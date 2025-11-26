import time, re, psutil
from platform import python_version
from sys import argv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler
from telegram.utils.helpers import escape_markdown, mention_html
from telegram.error import BadRequest, Unauthorized

from ShriBots import (
    OWNER_ID,
    OWNER_USERNAME,
    dispatcher, 
    StartTime,
    LOGGER,
    SUPPORT_CHAT,
    TOKEN,
    telethn,
    updater
)

from ShriBots.Plugins import ALL_MODULES
from ShriBots.__help__ import (
    get_help, 
    help_button, 
    get_settings, 
    settings_button, 
    migrate_chats, 
    send_help, 
    send_admin_help,
    send_user_help,
    user_help_button,
    send_settings,
    admin_help_button,
    tools_help_button,
    send_tools_help,
    HELP_STRINGS
)

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

PM_START_TEXT = """
Hello *{}*, My name is *{}*! 
A powerful Telegram group management bot with 70+ commands!

**Main Features:**
• Advanced Moderation
• Reporting System  
• Rules Management
• Notes & Filters
• Purge Messages
• User Info
• And much more!

*Add me to your group and make me admin!*
"""

def start(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    first_name = user.first_name
    
    if chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("stngs_"):
                # Settings handling
                pass
        else:
            message.reply_text(
                PM_START_TEXT.format(escape_markdown(first_name), escape_markdown(context.bot.first_name)),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="➕ Add to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
                    [InlineKeyboardButton(text="Admin", callback_data="admin_back"),
                     InlineKeyboardButton(text="Users", callback_data="user_back")],
                    [InlineKeyboardButton(text="Tools", callback_data="tools_back"),
                     InlineKeyboardButton(text="Help", callback_data="help_back")]
                ]),
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        uptime = get_readable_time((time.time() - StartTime))
        text = (
            f"Hello {mention_html(user.id, user.first_name)}, I'm {context.bot.first_name}\n\n"
            f"┏━━━━━━━━━━━━━━\n"
            f"┣ Owner: @{OWNER_USERNAME}\n"
            f"┣ Uptime: {uptime}\n"
            f"┣ Python: {python_version()}\n"
            f"┗━━━━━━━━━━━━━━"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="Support", url=f"https://t.me/{SUPPORT_CHAT}")]
        ])
        
        message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

def main():
    # Start handlers
    start_handler = CommandHandler("start", start, pass_args=True, run_async=True)
    help_handler = CommandHandler("help", get_help, run_async=True)
    
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    
    # Start the bot
    LOGGER.info("Bot started successfully!")
    updater.start_polling(drop_pending_updates=True)
    updater.idle()

if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    telethn.start(bot_token=TOKEN)
    main()
