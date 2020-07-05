from constants import *

def rgb2hex(rgb):
    return "#%02x%02x%02x" % rgb

def needless(text):
    return len(text) == 0 or DEFAULT_TEXT == text