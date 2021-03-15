from collections import defaultdict
from datetime import datetime, timedelta
from time import time
from random import randint
from re import search
from dotenv import load_dotenv
import os
from .cmds import games, misc, cmds_list
from .channeldata import KEYWORDS
from . import db

load_dotenv()
PREFIX=os.getenv("BOT_PREFIX")

welcomed = []
messages = defaultdict(int)

def process(bot, user, message):
    update_records(bot, user)
    if(message.startswith(PREFIX)):
        print("Comando")
        cmd=message.split(" ")[0][len(PREFIX):]
        args=message.split(" ")[1:]
        perform(bot, user, cmd, *args)
    else:
        print("Reacción")
        if user['id'] not in welcomed:
            welcome(bot, user)
        elif "bye" in message:
            say_goodbye(bot,user)
        for key, response in KEYWORDS.items():
            if key in message:
                bot.send_message(response)

        # if user['id'] != botId:
        check_activity(bot, user)

        # if(match := search(r'cheer[0-9]+',message)) is not None:
        #     thank_for_cheer(bot,user,match)

        if(h:= games.heist) is not None:
            if h.start_time <= time() and not h.running:
                games.run_heist(bot)
            elif h.end_time<= time() and h.running:
                games.end_heist(bot)

def perform(bot, user, call, *args):
    if call in ("help","commands","cmds"):
        misc.help(bot, PREFIX, cmds_list)
    else:
        for cmd in cmds_list:
            if cmd.permission == 'admin' and user['name'].lower()!= OWNER:
                print(f"{user['name']} intentó usar comandos de admin")
                return
            if call in cmd.callables:
                if time()>cmd.next_use:
                    cmd.func(bot, call, user,*args)
                    cmd.next_use=time()+cmd.cooldown

                else:
                    bot.send_message(f"Espera un poco e intenta de nuevo en {cmd.next_use-time():,.0f} segundos.")

                return

        bot.send_message(f"{user['name']}, \"{call}\" no es un comando registrado, puedes usar !help para saber qué puedes hacer :)")

def add_user(bot, user):
    db.execute("INSERT OR IGNORE INTO users (UserID, UserName) VALUES (?,?)",
    user['id'], user['name'].lower())

def update_records(bot, user):
    db.execute("UPDATE users SET UserName = ?, MessagesSent = MessagesSent +1 WHERE UserID = ?",
    user["name"].lower(), user["id"])
    
    stamp=db.field("select CoinLock FROM users WHERE UserID = ?",user['id'])

    if datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S") < datetime.utcnow():
        coinlock = (datetime.utcnow()+timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
        db.execute("UPDATE users SET Coins=Coins + ?, CoinLock=? WHERE UserID=?;", 
        randint(1,5), coinlock, user['id'])

def welcome(bot, user):
    bot.send_message(f"¡Hola {user['name']}! Espero disfrutes el stream ❤︎ ❤︎ ❤︎")
    welcomed.append(user['id'])

def say_goodbye(bot, user):
    bot.send_message(f"Cya leita {user['name']}, feraligeita")
    welcomed.remove(user['id'])

def check_activity(bot, user):
    messages[user['id']] += 1

    if(count :=  messages[user['id']]%20) == 0:
        bot.send_message(f"¡Wow! Gracias por ser tan activo en el chat {user['name']}, has enviado {messages[user['id']]} mensajes")

# def thank_for_cheer(bot, user, match):
#     bot.send_message(f"Thanks for the {match.group[5:],} bits {user}! That's really appreciated!")