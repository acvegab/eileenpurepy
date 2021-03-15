
from dotenv import load_dotenv
from bot import Bot
import os

load_dotenv()

if __name__ == "__main__":
    USERNAME = os.getenv('BOT_NAME').lower()
    OWNER = os.getenv('OWNER').lower()
    CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
    TOKEN = os.getenv('TWITCH_TOKEN')
    CHANNEL = f"#{OWNER}"
    bot = Bot(OWNER, USERNAME, CLIENT_ID, TOKEN, CHANNEL)
    bot.start()