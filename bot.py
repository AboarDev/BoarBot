import discord
from commands import Commands
import asyncio
import json
import io

Configfile = 'F:/Pyth/BoarBot/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        self.commands = Commands()
        self.config = json.loads(open(Configfile).read())
        self.restart = False

    async def on_ready(self):
        print(F'Logged in as\n{self.user.name}, {self.user.id}\n------')
        await self.change_presence(activity=discord.Game(self.config['status']))

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content[0:1] == '+':
            splitContent = str.split(message.content[1:])
            theCommand = splitContent[0]
            if theCommand in self.commands.theCommands:
                aCommand = self.commands.theCommands[theCommand]
                if aCommand['requiresAuth'] and self.isAuthed(message.author.id):
                    asyncio.create_task(aCommand['method'](self, message, message.content.replace(F"+{theCommand} ", '')))
                else:
                    await message.channel.send('🔒 Must be authed to use command')
        else:
            print(message.author.id)
            theId = str(message.author.id)
            if theId in self.config['users']:
                self.config['users'][theId]['exp'] += 10
                print(self.config['users'][theId]['exp'])
            else:
                self.config['users'][theId] = {}
                self.config['users'][theId]['exp'] = 10
            

    async def setStatus(self, newStatus):
        await self.change_presence(activity=discord.Game(newStatus))
        self.config['status'] = newStatus

    async def close(self):
        open(Configfile, 'w').write(json.dumps(self.config, indent=2))
        await discord.Client.close(self)

    def isAuthed(self, user):
        return user in self.config['authedUsers']

    def saveFile(self,content,filename,folder='scraped'):
        theJson = json.dumps(content, indent=2)
        open(F'F:/Pyth/BoarBot/{folder}/{filename}.json','w').write(theJson)

    async def pushFile(self,channel,content):
        theJson = json.dumps(content, indent=2)
        theBin = io.BytesIO(theJson.encode('utf8'))
        await channel.send(channel.name,file=discord.File(theBin,filename = f"{channel.name}.json"))
