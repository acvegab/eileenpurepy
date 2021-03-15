from time import time
from . import mod, misc, economy, games

class Cmd(object):
    def __init__(self, callables, func, cooldown=0, permission='public'):
        self.callables=callables
        self.func=func
        self.cooldown=cooldown
        self.next_use = time()
        self.permission = permission

cmds_list=[
    Cmd(["hello","hi","hey","hola"], misc.hello, cooldown=15),
    Cmd(["discord","twitter","facebook","instagram"], misc.social),
    Cmd(["coinflip","flip"], games.coinflip,cooldown=0),
    Cmd(["heist"], games.start_heist,cooldown=10),
    Cmd(["coins"], economy.coins),
    Cmd(["shoutout","so"], mod.shoutout),
    Cmd(["warn"], mod.warn),
    Cmd(["unwarn", "rmwarn"],mod.remove_warn),
]