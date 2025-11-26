import importlib
import re
import ShriBots

from ShriBots import LOGGER, dispatcher
from ShriBots.__help__ import IMPORTED, MIGRATEABLE, HELPABLE, ADMIN, USER, TOOLS

def __list_all_modules():
    import glob
    from os.path import basename, dirname, isfile
    import os
    
    path = './ShriBots/Plugins/'
    list_of_files = []
    
    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    
    all_modules = [
        basename(f)[:-3]
        for f in list_of_files
        if isfile(f) and f.endswith('.py') and not f.endswith('__init__.py')
    ]
    
    return all_modules

ALL_MODULES = __list_all_modules()
LOGGER.info("Modules loaded: %s", str(ALL_MODULES))
__all__ = ALL_MODULES + ["ALL_MODULES"]
