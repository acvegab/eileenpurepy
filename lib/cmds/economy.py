from .. import db


def coins(bot, call, user, *args):
    coins = db.field("SELECT Coins FROM users WHERE UserID = ?;",
    user['id'])

    bot.send_message(f"{user['name']}, tienes {coins:,} monedas.")