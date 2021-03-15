from irc.bot import SingleServerIRCBot
from requests import get
from lib import db, react, automod


class Bot(SingleServerIRCBot):
    def __init__(self, owner, username, client_id, token, channel):
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.OWNER = owner
        self.USERNAME = username
        self.CLIENT_ID = client_id
        self.TOKEN = token
        self.CHANNEL = channel

        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID":self.CLIENT_ID, "Accept":"application/vnd.twitchtv.v5+json"}
        resp = get(url, headers=headers).json()
        self.channel_id = resp["users"][0]["_id"]

        super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")],self.USERNAME,self.USERNAME)


    def on_welcome(self,cxn, event):
        for req in ("membership", "tags", "commands"):
            cxn.cap("REQ",f":twitch.tv/{req}")

        cxn.join(self.CHANNEL)
        db.build();
        print("Now online")
        self.send_message("Now online.")

    @db.with_commit
    def on_pubmsg(self, cxn, event):
        tags = {kvpair["key"]:kvpair["value"] for kvpair in event.tags}
        user = {"name" : tags["display-name"],"id":tags["user-id"]}
        if user["name"] == self.USERNAME:
            return

        message = event.arguments[0]
        react.add_user(self, user)
        print(f"Message from {user['name']}:{message}")

        if automod.clear(self, user, message):
            react.process(self, user, message)
            

    def send_message(self, message):
        self.connection.privmsg(self.CHANNEL,message)

