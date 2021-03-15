from .. import db
warning_timers = (1, 5, 60)
def admin(func):
    def inner(*args, **kwargs):
        if args[2]['name'].lower() != args[0].OWNER:
            print(f"{args[2]['name'].lower()} trató de usar un comando de admin")
            return
        func(*args, **kwargs)
    return inner

@admin
def warn(bot, cmd, user, target=None, *reason):
    if target is None:
        bot.send_message("Debes especificar un usuario")
    else:
        reason = " ".join(reason)
        warnings=db.field("SELECT Warnings FROM users WHERE UserName = ?",
        target.lower())

        if warnings is None:
            bot.send_message("Ese usuario no ha visitado el canal aún")
        elif warnings < len(warning_timers):
            mins = warning_timers[warnings]
            # bot.send_message(f"/timeout {target} {mins}m")
            bot.send_message(f"{target}, has sido silenciado por la razón siguiente: {reason}. Podrás enviar mensajes en {mins} minuto(s).")

            db.execute("UPDATE users SET Warnings = Warnings + 1 WHERE UserName = ?",
            target)

        else:
            # bot.send_message(f"/ban {target} Repeated infractions.")
            bot.send_message(f"{target}, has sido baneado del chat por repetidas infracciones.")

@admin
def remove_warn(bot, cdm, user, target=None, *args):
    if target:
        warnings = db.field("SELECT Warnings FROM users WHERE UserID = ?",
        user['id'])
        if warnings <= 0:
            bot.send_message(f"{target} no ha recibido ningún warning")
        else:
            db.execute("UPDATE users SET Warnings = Warnings - 1 WHERE UserName = ?",
            target)
        
        bot.send_message(f"Los warnings de {target} han sido removidos.")
    else:
        bot.send_message(f"{user['name']}, debes especificar un usuario.")
        
@admin
def shoutout(bot, call, user, *args):
    if args==():
        bot.send_message(f"Vuelve a intentarlo agregando el usuario. Ej. !so satokito")
        return 
    bot.send_message(f"Visiten a {args[0]} en su canal https://www.twitch.tv/{args[0].lower()} y denle mucho amor ❤︎ ❤︎ ❤︎")

@admin
def shutdown(bot, cmd, user, *args):
    if user["name"].lower() == OWNER:
        bot.send_message("Shutting down.")
        db.commit()
        db.close()
        bot.disconnect()
        exit(0)
    else:
        bot.send_message("No puedes apagarme uwu")
