import asyncio
import module_base
import userlevels
import json
import re


class User(userlevels.User):

    def __init__(self, theId, theExp, theCoins, theLevel):
        userlevels.User.__init__(self, theId, theExp, theCoins, theLevel)

    def onMessage(self, boost=0):
        self.exp += 1
        if self.exp % 10 == 0:
            self.coins += 1


class Coins(userlevels.UserLevels):

    def __init__(self, client):
        self.numberRegex = re.compile(r"\d+\.?\d*")
        self.users = []
        self.client = client
        self.theCommands = {
            "coins": {'method': self.coins, 'requiresAuth': False},
            "send": {'method': self.send, 'requiresAuth': False}
        }
        self.client.addLoader(self.on_ready)
        self.client.addHandler(self.on_message)
        self.client.addCommands(self.theCommands)
        self.client.addTeardown(self.on_close)
        theUsers = json.loads(open("config/users.json").read())
        for user in theUsers:
            self.users.append(
                User(user["id"], user["exp"], user["coins"], user["level"]))

    def on_ready(self):
        pass

    async def on_message(self, msg):
        theId = msg.author.id
        aUser = self.getUser(theId)
        if not aUser and msg.author.bot == False:
            aUser = self.addUser(theId)
        if aUser:
            aUser.onMessage()

    def on_close(self):
        userlevels.UserLevels.outputUsers()
        self.client.saveFile(self.outputUsers(),"users","config")

    async def coins(self, msg, txt):
        user = self.getUser(msg.author.id)
        if not user:
            user = self.addUser(msg.author.id)
        await msg.channel.send(f'```{str(user.coins)} BoarCoins```')


    async def send(self, msg, txt):
        amount = 0
        split = txt.split(' ')
        for word in split:
            if self.numberRegex.match(word):
                amount = int(word)
        target = msg.mentions[0]
        recievingUser = self.getUser(target.id)
        if not recievingUser:
            recievingUser = self.addUser(target.id)
        sendingUser = self.getUser(msg.author.id)
        if sendingUser and sendingUser.coins >= amount and amount > 0:
            sendingUser.coins -= amount
            recievingUser.coins += amount
            await msg.channel.send(f"Sent {str(amount)} boarcoins to {target.name}#{target.discriminator}")
        