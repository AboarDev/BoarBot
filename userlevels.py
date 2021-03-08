import json
import asyncio


class UserLevels():

    def __init__(self, client):
        self.users = []
        self.client = client
        self.theCommands = {

        }
        self.client.addCommands(self.theCommands)
        self.client.addHandler(self.on_message)
        self.client.addLoader(self.on_ready)
        theUsers = json.loads(open("config/users.json").read())
        for user in theUsers:
            self.users.append(
                User(user["id"], user["exp"], user["coins"], user["level"], user["expRate"]))

    def on_ready(self):
        pass

    async def on_message(self, msg):
        theId = msg.author.id
        aUser = self.getUser(theId)
        if not aUser and msg.author.bot == False:
            aUser = self.addUser(theId)
        if aUser and aUser.onMessage():
            message = f'`{message.author.display_name}#{message.author.discriminator}` Reached level {aUser.level}!'

    def getUser(self, id):
        return next((x for x in self.users if x.id == id), False)

    def addUser(self, id):
        theUser = User(id, 0, 0, 0)
        self.users.append(theUser)
        return theUser

    def outputUsers(self):
        out = []
        for aUser in self.users:
            out.append(aUser.__dict__)
        out.sort(key=lambda r: r["exp"], reverse=True)
        out.sort(key=lambda r: r["level"], reverse=True)
        return out

    def __str__(self):
        pass


class User():

    def __init__(self, theId, theExp, theCoins, theLevel, theExpRate=1):
        self.id = theId
        self.exp = theExp
        self.coins = theCoins
        self.level = theLevel
        self.expRate = theExpRate
        self.guilds = []

    def onMessage(self, boost=0):
        self.exp += (1 * self.expRate) + boost
        if self.exp >= (self.level + 1)*1000:
            self.level += 1
            self.exp = self.exp - (self.level*1000)
            self.coins += 10
            return True
        else:
            return False

    def __str__(self):
        pass
