import re
from html import escape
from telegram import MessageEntity
from telegram.utils.helpers import escape_markdown

def markdown_parser(txt, entities=None, offset=0):
    if not entities:
        entities = []
    if not txt:
        return ""
    
    prev = 0
    res = ""
    for ent in entities:
        if ent.offset < -offset:
            continue
        start = ent.offset + offset
        end = ent.offset + offset + ent.length
        
        if start < prev:
            continue
        res += txt[prev:start]
        
        if ent.type == MessageEntity.BOLD:
            res += "*" + txt[start:end] + "*"
        elif ent.type == MessageEntity.ITALIC:
            res += "_" + txt[start:end] + "_"
        elif ent.type == MessageEntity.CODE:
            res += "`" + txt[start:end] + "`"
        elif ent.type == MessageEntity.PRE:
            res += "```" + txt[start:end] + "```"
        elif ent.type == MessageEntity.URL:
            res += "[{}]({})".format(txt[start:end], txt[start:end])
        elif ent.type == MessageEntity.TEXT_LINK:
            res += "[{}]({})".format(txt[start:end], ent.url)
        else:
            res += txt[start:end]
        prev = end
    
    res += txt[prev:]
    return res
