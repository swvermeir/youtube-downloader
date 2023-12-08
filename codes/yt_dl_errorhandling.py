import logging
import sys
import yt_dlp
from typing import Callable


def lineno():  # does this actually work???
    return sys._getframe().f_lineno


def while_errorhandling(func: Callable, extra_error_message: str = "", max_tries: int = None):
    def basic_error_stuf(err, i):
        if hasattr(err, 'usermessage_text') and err.usermessage_text:
            logging.error(f"[line {lineno()}][attempt {i}/{max_tries}] {err.usermessage_text} ({extra_error_message})")
        else:
            logging.error(f"[line {lineno()}][attempt {i}/{max_tries}] {err} ({extra_error_message})")
    
    def inner_function(*func_args, **func_kwargs):
        i = 1
        while max_tries is None or i < max_tries:
            try:
                return func(*func_args, **func_kwargs)
            except yt_dlp.utils.YoutubeDLError as err:
                basic_error_stuf(err, i)
            i += 1
        return func(*func_args, **func_kwargs)  # final try => raise exception if needed
    return inner_function
