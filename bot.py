import discord
import asyncio
import json
import io

Configfile = 'config/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        #self.theLevels = userlevels.UserLevels()
        self.config = json.loads(open(Configfile).read())
        self.restart = False
        self.levelChannel = None
        self.loadedLevels = False
        self.commands = {}

    async def on_ready(self):
        print(F'Logged in as\n{self.user.name}, {self.user.id}\n------')
        await self.change_presence(activity=discord.Game(self.config['status']))
        """ theUsers = json.loads(open("config/users.json").read())
        if self.loadedLevels == False:
            for user in theUsers:
                if not self.theLevels.getUser(user["id"]):
                    self.theLevels.users.append(userlevels.User(user["id"],user["exp"],user["coins"],user["level"],user["expRate"]))
            self.levelChannel = await self.fetch_channel(self.config['levelUpChannel'])
            self.loadedLevels = True """

    async def on_message(self, message):
        if message.author.bot == True:
            return
        if message.content[0:1] == '+':
            splitContent = str.split(message.content[1:])
            theCommand = splitContent[0]
            if theCommand in self.commands:
                aCommand = self.commands[theCommand]
                if (aCommand['requiresAuth'] and self.isAuthed(message.author.id)) or (aCommand['requiresAuth'] == False):
                    asyncio.create_task(aCommand['method'](
                        message, message.content.replace(F"+{theCommand} ", '')))
                else:
                    await message.channel.send('🔒 Must be authed to use command')
        """ elif message.guild.id in self.config['levelEnabled']:
            theId = message.author.id
            aUser = self.theLevels.getUser(theId)
            if not aUser and message.author.bot == False:
                aUser = self.theLevels.addUser(theId)
            if aUser and aUser.onMessage():
                await self.levelChannel.send(f'`{message.author.display_name}#{message.author.discriminator}` Reached level {aUser.level}!') """

    async def setStatus(self, newStatus):
        await self.change_presence(activity=discord.Game(newStatus))
        self.config['status'] = newStatus

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
