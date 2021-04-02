import asyncio
import module_base
import json
import re


class User():

    def __init__(self, theId, theExp, theCoins, theLevel, items = []):
        self.id = theId
        self.exp = theExp
        self.coins = theCoins
        self.level = theLevel
        self.items = items

    def onMessage(self, boost=0):
        self.exp += 1
        if self.exp % 10 == 0:
            self.coins += 1


class Item():

    def __init__(self, name, desciption, price):
        self.name = name
        self.desciption = desciption
        self.price = price

    def __str__(self):
        return f'{self.name} - ${self.price} -  {self.desciption}\n'


class Coins(module_base.module_base):

    def __init__(self, client):
        self.numberRegex = re.compile(r"\d+\.?\d*")
        self.users = []
        self.client = client
        self.theCommands = {
            "coins": {'method': self.coins, 'requiresAuth': False},
            "send": {'method': self.send, 'requiresAuth': False},
            "buy": {'method': self.buy, 'requiresAuth': False},
            "market": {'method': self.market, 'requiresAuth': False},
            "throw": {'method': self.throw, 'requiresAuth': False},
            "items": {'method': self.items, 'requiresAuth': False}
        }
        self.buyable = {
            "token": Item("Token","Allows use of msg command", 10),
            "pre-order": Item("Pre-Order","TBA", 5),
            "egg": Item("Egg","An Egg",1)
        }
        self.client.addLoader(self.on_ready)
        self.client.addHandler(self.on_message)
        self.client.addCommands(self.theCommands)
        self.client.addTeardown(self.on_close)
        theUsers = json.loads(open("config/users.json").read())
        for user in theUsers:
            self.users.append(
                User(user["id"], user["exp"], user["coins"], user["level"], user["items"]))

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
        self.outputUsers()
        self.client.saveFile(self.outputUsers(),"users","config")

    def outputUsers(self):
        out = []
        for aUser in self.users:
            out.append(aUser.__dict__)
        out.sort(key=lambda r: r["exp"], reverse=True)
        out.sort(key=lambda r: r["level"], reverse=True)
        return out

    def addUser(self, id):
        theUser = User(id, 0, 10, 0)
        self.users.append(theUser)
        return theUser

    def getUser(self, id):
        return next((x for x in self.users if x.id == id), False)

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
            await msg.channel.send(f"```Sent {str(amount)} boarcoins to {target.name}#{target.discriminator}```")

    async def buy(self, msg, txt):
        user = self.getUser(msg.author.id)
        if not user:
            user = self.addUser(msg.author.id)
        item = txt.split(" ")[0]
        if item in self.buyable:
            if user.coins >= self.buyable[item].price:
                user.items.append(item)
                user.coins -= self.buyable[item].price
                await msg.channel.send(f"```Bought {item}```")

    async def market(self, msg, txt):
        out = ""
        for x in self.buyable:
            out += self.buyable[x].__str__()
        await msg.channel.send(f"```{out}```")

    async def throw(self, msg, txt):
        user = self.getUser(msg.author.id)
        if not user:
            user = self.addUser(msg.author.id)
        if "egg" in user.items:
            user.items.remove("egg")
            if len(msg.mentions > 0):
                target = msg.mentions[0]
                await msg.channel.send(f"```Threw Egg at {target.name}#{target.discriminator}```")
            else:
                await msg.channel.send(f"```Threw Egg at a cloud```")

    async def items(self, msg, txt):
        user = self.getUser(msg.author.id)
        if not user:
            user = self.addUser(msg.author.id)
        out = ""
        for item in user.items:
            out += item
            out += '\n'
        await msg.channel.send(f"```{out}```")