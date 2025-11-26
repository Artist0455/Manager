from math import ceil
from telegram import InlineKeyboardButton

def paginate_modules(page_n, module_dict, prefix, chat=None):
    modules = sorted([mod for mod in module_dict.keys()])
    
    pairs = []
    pair = []
    
    for module in modules:
        pair.append(InlineKeyboardButton(
            text=module_dict[module].__mod_name__,
            callback_data="{}_module({})".format(prefix, module),
        ))
        
        if len(pair) > 1:
            pairs.append(pair)
            pair = []
    
    if pair:
        pairs.append(pair)
    
    max_pages = ceil(len(pairs) / 7)
    modulo_page = page_n % max_pages
    
    if len(pairs) > 7:
        pairs = pairs[modulo_page * 7: 7 * (modulo_page + 1)] + [
            [
                InlineKeyboardButton(
                    "⬅️", callback_data="{}_prev({})".format(prefix, modulo_page)
                ),
                InlineKeyboardButton(
                    "➡️", callback_data="{}_next({})".format(prefix, modulo_page)
                ),
            ]
        ]
    
    return pairs
