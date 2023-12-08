import logging
import sys
import yt_dlp
from typing import Callable
import os


def while_errorhandling(func: Callable, extra_error_message: str = "", max_tries: int = None):
    def basic_error_stuf(err, i):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        line = exc_tb.tb_lineno
        base_message = err.usermessage_text if hasattr(err, 'usermessage_text') and err.usermessage_text else err
        logging.warning(f"[{exc_type}][file {fname}][line {line}][attempt {i}/{max_tries}] {base_message} ({extra_error_message})")
    
    def inner_function(*func_args, **func_kwargs):
        i = 1
        while max_tries is None or i < max_tries:
            try:
                return func(*func_args, **func_kwargs)
            except yt_dlp.utils.DownloadError as err:  # invalid filename
                return err
            except yt_dlp.utils.YoutubeDLError as err:
                basic_error_stuf(err, i)
            i += 1
        return func(*func_args, **func_kwargs)  # final try => raise exception if needed
    return inner_function
