import discord
import asyncio
import json
import io

Configfile = 'config/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        self.config = json.loads(open(Configfile).read())
        self.restart = False
        self.commands = {}
        self.messageHandlers = []
        self.loaders = []
        self.closers = []

    async def on_ready(self):
        print(F'Logged in as\n{self.user.name}, {self.user.id}\n------')
        await self.change_presence(activity=discord.Game(self.config['status']))
        for loader in self.loaders:
            loader()
        """ self.levelChannel = await self.fetch_channel(self.config['levelUpChannel'])
            self.loadedLevels = True """

    async def on_message(self, message):
        if message.author.bot == True:
            return
        elif message.content[0:1] == '+':
            splitContent = str.split(message.content[1:])
            theCommand = splitContent[0]
            if theCommand in self.commands:
                aCommand = self.commands[theCommand]
                if (aCommand['requiresAuth'] and self.isAuthed(message.author.id)) or (aCommand['requiresAuth'] == False):
                    asyncio.create_task(aCommand['method'](
                        message, message.content.replace(F"+{theCommand} ", '')))
                else:
                    await message.channel.send('🔒 Must be authed to use command')
        else:
            for handler in self.messageHandlers:
                handler(message)

    async def setStatus(self, newStatus):
        await self.change_presence(activity=discord.Game(newStatus))
        self.config['status'] = newStatus

    async def saveConfig (self):
        self.saveFile(self.config, "config", "config")

    async def close(self):
        try:
            self.saveFile(self.config, "config", "config")
            # self.saveFile(self.theLevels.outputUsers(),"users","config")
        finally:
            await discord.Client.close(self)

    def isAuthed(self, user):
        return user in self.config['authedUsers']

    def saveFile(self, content, filename, folder='scraped'):
        theJson = json.dumps(content, indent=2)
        open(F'{folder}/{filename}.json', 'w').write(theJson)

    async def pushFile(self, channel, content):
        theJson = json.dumps(content, indent=2)
        theBin = io.BytesIO(theJson.encode('utf8'))
        await channel.send(channel.name, file=discord.File(theBin, filename=f"{channel.name}.json"))

    def addCommands(self, commands):
        self.commands.update(commands)
    
    def addLoader(self, loader):
        self.loaders.append(loader)

    def addHandler(self,handler):
        self.messageHandlers.append(handler)
