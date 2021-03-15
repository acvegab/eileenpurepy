
from datetime import datetime
from sys import exit
from time import time
from .. import db
from ..channeldata import SOCIAL_URL

BOOT_TIME = time()

def help(bot, prefix, cmds):
    # bot.send_message("Registered commands: " + ", ".join([f"{prefix}{cmd}" for cmd in sorted(cmds.keys())]))
    # bot.send_message("Registered commands: "
    # + ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

    bot.send_message(f"Comandos registrados (incl. aliases): "
    + ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

def hello(bot, call, user, *args):
    bot.send_message(f"Hola {user['name']}!")

def social(bot, call, user,*args):
    bot.send_message(f"Hola {user['name']}! Puedes encontrar a Satokito en {call} {SOCIAL_URL[call]} ❤︎ ❤︎ ❤︎")
    
def about(bot, cmd, user, *args):
    bot.send_message("Version 1.0.0. Developed by Carolina. Special thanks to Carberra (Parafoxia) for the help")

def uptime(bot, user, *args):
    bot.send_message(f"The bot has been online for {timedelta(seconds=time()-BOOT_TIME)}.")

def userinfo(bot, cmd, user, *args):
    bot.send_message(f"Name: {user['name']}. ID: {user['id']}.")































    # 'anuncios parroquiales':[
    #             '¡Holi! No olvides seguir a Satokito en twitter https://twitter.com/Satokito y en instagram https://www.instagram.com/cartulain ❤︎ ❤︎ ❤︎',
    #             '¿Ya sigues a Satokito en sus redes? Síguela en twitter https://twitter.com/Satokito y en instagram https://www.instagram.com/cartulain ❤︎ ❤︎ ❤︎',
    #             'Sigue a Satokito en facebook https://www.facebook.com/Satokitoplz ❤︎ ❤︎ ❤︎'
    #             ],