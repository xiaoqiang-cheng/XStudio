import os
from qtpy.QtUiTools import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *
from qtpy.QtGui import *
import qtpy as GuiCoreLib
import sys
import re
import json

__GUICOREVERSION__ = "qtpy"
# Regular expression for comments
comment_re = re.compile(
    '(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
    re.DOTALL | re.MULTILINE
)

def parse_json(filename):

    with open(filename, encoding="utf-8") as f:
        content = ''.join(f.readlines())
        match = comment_re.search(content)
        while match:
            content = content[:match.start()] + content[match.end():]
            match = comment_re.search(content)

    return json.loads(content)
