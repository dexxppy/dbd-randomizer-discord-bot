import sys
import asyncio
import traceback
import logging

ERROR_FILE = "last_error.txt"

def save_error(error_msg: str):
    with open(ERROR_FILE, "w", encoding="utf-8") as f:
        f.write(error_msg)

def log_exception(exc_type, exc_value, exc_traceback):
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    save_error(error_msg)

sys.excepthook = log_exception

def handle_async_exception(loop, context):
    exception = context.get("exception")
    if exception:
        error_msg = "".join(
            traceback.format_exception(
                type(exception),
                exception,
                exception.__traceback__
            )
        )
    else:
        error_msg = str(context)

    save_error(error_msg)

class DiscordLogHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            save_error(self.format(record))

discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.ERROR)
discord_logger.addHandler(DiscordLogHandler())
