import importlib, re
from ShriBots import dispatcher, ALLOW_EXCL, LOGGER
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from ShriBots.Handlers.misc import paginate_modules
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown
from ShriBots.Handlers.validation import is_user_admin
from telegram.ext.dispatcher import DispatcherHandlerStop
from os.path import isfile

HELP_STRINGS = """
Hey there! My name is *{}*.
I'm a modular group management bot with 70+ features!

*Main Categories:*
• Admin - Moderation commands
• User - General user commands  
• Tools - Utility functions
""".format(dispatcher.bot.first_name)

IMPORTED = {}
ADMIN_IMPORTED = {}
USER_IMPORTED = {}
TOOLS_IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
ADMIN = {}
USER = {}
TOOLS = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

import os
path = './ShriBots/Plugins/'
list_of_files = []

for root, dirs, files in os.walk(path):
    for file in files:
        list_of_files.append(os.path.join(root, file))

mod_name = [
    name[:-3].replace("/", ".").replace("\\", ".")
    for name in list_of_files
    if isfile(name) and name.endswith(".py") and not name.endswith("__init__.py")
]

for module_name in mod_name:
    imported_module = importlib.import_module(module_name)
    
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard,
    )

def help_button(update: Update, context: CallbackContext):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="help_back")]]),
            )
        elif query.data == "help_back":
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")),
            )
        context.bot.answer_callback_query(query.id)
    except BadRequest:
        pass

def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat
    args = update.effective_message.text.split(None, 1)

    if chat.type != chat.PRIVATE:
        update.effective_message.reply_text(
            "Contact me in PM for help!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text="Help", url=f"t.me/{context.bot.username}?start=help")
            ]])
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = f"Help for *{HELPABLE[module].__mod_name__}*:\n" + HELPABLE[module].__help__
        send_help(chat.id, text)
    else:
        send_help(chat.id, HELP_STRINGS)
