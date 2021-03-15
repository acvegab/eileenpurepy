from collections import defaultdict
from . import db
from .channeldata import CURSES, WARNING_TIMERS

def clear(bot, user, message):
    if any([curse in message for curse in CURSES]):
        warn(bot, user, reason="Cursing")
        return False
    return True

def warn(bot, user, *, reason=None):
    warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?",
    user["id"])

    if warnings < len(warning_timers):
        mins = warning_timers[warnings]
        # bot.send_message(f"/timeout {user['name']} {mins}m")
        bot.send_message(f"{user['name']} has sido silenciado por la siguiente razón: {reason}. Podrás escribir de nuevo en {mins} minuto(s)")

        db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserID = ?",
        user['id'])

    else:
        # bot.send_message(f"/ban {user['name']} Repeated infractions.")
        bot.send_message(f"{user['name']} has sido baneado del chat por repetidas infracciones.")
