import logging
from ssl import SSLError
import sys
import yt_dlp


def lineno():
    return sys._getframe().f_lineno


def while_errorhandling(func, *func_args, extra_error_message="", max_tries=3, **func_kwargs):
    def basic_error_stuf(err, i):
        if hasattr(err, 'usermessage_text') and err.usermessage_text:
            logging.error(f"[line {lineno()}][attempt {i}/{max_tries}] {err.usermessage_text} ({extra_error_message})")
        else:
            logging.error(f"[line {lineno()}][attempt {i}/{max_tries}] {err} ({extra_error_message})")

    i = 0
    while i < max_tries:
        i += 1
        try:
            x = func(*func_args, **func_kwargs)
            return x if x is not None else True
        except yt_dlp.utils.YoutubeDLError as err:
            basic_error_stuf(err, i)
    return None
