import discord
from commands import Commands
import asyncio
import json
import io
import userlevels

Configfile = 'config/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        self.theLevels = userlevels.UserLevels()
        self.commands = Commands(self.theLevels)
        self.config = json.loads(open(Configfile).read())
        self.restart = False
        self.levelChannel = None

    async def on_ready(self):
        print(F'Logged in as\n{self.user.name}, {self.user.id}\n------')
        await self.change_presence(activity=discord.Game(self.config['status']))
        theUsers = json.loads(open("config/users.json").read())
        for user in theUsers:
            self.theLevels.users.append(userlevels.User(user["id"],user["exp"],user["coins"],user["level"]))
        self.levelChannel = await self.fetch_channel(self.config['levelUpChannel'])

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content[0:1] == '+':
            splitContent = str.split(message.content[1:])
            theCommand = splitContent[0]
            if theCommand in self.commands.theCommands:
                aCommand = self.commands.theCommands[theCommand]
                if (aCommand['requiresAuth'] and self.isAuthed(message.author.id)) or (aCommand['requiresAuth'] == False):
                    asyncio.create_task(aCommand['method'](self, message, message.content.replace(F"+{theCommand} ", '')))
                else:
                    await message.channel.send('🔒 Must be authed to use command')
        elif message.guild.id in self.config['levelEnabled']:
            theId = message.author.id
            aUser = self.theLevels.getUser(theId)
            if not aUser:
                aUser = self.theLevels.addUser(theId)
            if aUser.onMessage():
                self.levelChannel.send(f'{message.author.display_name}#{message.author.discriminator} Leveled Up!')

    async def setStatus(self, newStatus):
        await self.change_presence(activity=discord.Game(newStatus))
        self.config['status'] = newStatus

    async def close(self):
        #open(Configfile, 'w').write(json.dumps(self.config, indent=2))
        self.saveFile(self.config,"config","config")
        self.saveFile(self.theLevels.outputUsers(),"users","config")
        await discord.Client.close(self)

    def isAuthed(self, user):
        return user in self.config['authedUsers']

    def saveFile(self,content,filename,folder='scraped'):
        theJson = json.dumps(content, indent=2)
        open(F'{folder}/{filename}.json','w').write(theJson)

    async def pushFile(self,channel,content):
        theJson = json.dumps(content, indent=2)
        theBin = io.BytesIO(theJson.encode('utf8'))
        await channel.send(channel.name,file=discord.File(theBin,filename = f"{channel.name}.json"))
