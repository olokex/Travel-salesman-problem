#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from constants import *


def rgb2hex(rgb):
    """Provides RGB interpretation to hex one.
    Tkinter allows only hex or by word colors.
    """
    return "#%02x%02x%02x" % rgb


def needless(text):
    """Check if coordinates' text is empty or with default text."""
    return len(text) == 0 or DEFAULT_TEXT == text