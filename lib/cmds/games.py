from random import choice, randint
from time import time
from .. import db


heist=None
heist_lock=time()

def coinflip(bot, cmd, user, side=None, *args):
    if side is None:
        bot.send_message("Debes escoger un lado de la moneda, aguila o sol. Ej. !flip aguila")

    elif (side:=side.lower()) not in (opt:=("a","s","aguila","sol")):
        bot.send_message("Escoge una de las siguientes opciones: "+", ".join(opt))
    
    else:
        result = choice(("aguila","sol"))

        if side[0] == result[0]:
            db.execute("UPDATE users SET Coins = Coins + 10 WHERE UserID = ?",
            user['id'])
            bot.send_message(f"Es {result}! Ganaste 10 coins!")

        else:
            bot.send_message(f"Chale, cayó {result}. No ganaste :(")

        
class Heist(object):
    def __init__(self):
         self.users = []
         self.running = False
         self.start_time = time() + 60
         self.end_time = 0
         self.messages = {
             "success":[
                 "{} luchó contra los guardias y consiguió el botín!",
                 "{} se escabulló por la entrada trasera con su parte del botín!",
                 "{} entró y salió sin problemas con su dinero!"
             ],
             "fail":[       
                 "{} fue atrapad@ por los guardias!",
                 "{} recibió un disparo!",
                 "{} se perdió!"
             ]
         }

    def add_user(self, bot, user, bet):
        if self.running:
            bot.send_message("Un asalto está en progreso. Tendrás que esperar hasta el siguiente.")
        if user in self.users:
            bot.send_message("Ya estás listo para irte.")
        elif bet > (coins := db.field("SELECT Coins FROM users WHERE UserID =?", user['id'])):
            bot.send_message("No tienes suficiente para apostar, solo tienes {coins:,} monedas")
        else:
            db.execute("UPDATE users SET Coins = Coins - ? WHERE UserID = ?",
            bet, user["id"])
            self.users.append((user, bet))
            bot.send_message("Todo listo! Espera un poco a que comience el show...")



    def start(self, bot):
        bot.send_message("El asalto ha iniciado! Espera por los resultados...")
        self.running = True
        self.end_time = time() + randint(30,60)
    
    def end(self, bot):
        succeeded = []
        for user, bet in self.users:
            if randint(0,1):
                db.execute("UPDATE users SET Coins = Coins + ? WHERE UserID = ?",
                bet*1.5, user["id"])
                succeeded.append((user,bet*1.5))
                bot.send_message(choice(self.messages["success"]).format(user["name"]))
            else:
                bot.send_message(choice(self.messages["fail"]).format(user["name"]))
        if len(succeeded)>0:
            bot.send_message("El asalto terminó! Los ganadores: "+
            ", ".join([f"{user['name']}({coins:,} coins)" for user, coins in succeeded]))
        else:
            bot.send_message("El asalto salió mal, nadie logró escapar!")

        

def start_heist(bot, cmd, user, bet=None, *args):
    global heist
    if bet is None:
        bot.send_message("Necesitas especificar una cantidad para la apuesta. Ej. !heist 5")
    else:
        try:
            bet=int(bet)
        except ValueError:
            bot.send_message("Esa no es una apuesta válida")
        else:
            if bet < 1:
                bot.send_message("Debes apostar al menos 1 moneda.")
            else:
                if heist is None:
                    heist=Heist()
                heist.add_user(bot,user, bet)

def run_heist(bot):
    heist.start(bot)

def end_heist(bot):
    global heist
    heist.end(bot)
    heist = None


        
