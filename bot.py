import discord
from commands import Commands
import asyncio
import json

Configfile = 'F:/Pyth/BoarBot/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        self.commands = Commands()
        self.config = json.loads(open(Configfile).read())
        self.restart = False

    async def on_ready(self):
        print(F'Logged in as\n{self.user.name}, {self.user.id}\n------')
        await self.change_presence(activity=discord.Game('+now Kek'))

    async def on_message(self, message):
        if message.author.id == 469303587357327360:
            return
        if message.content[0:1] == '+':
            splitContent = str.split(message.content[1:])
            theCommand = splitContent[0]
            if theCommand in self.commands.aliases:
                asyncio.create_task(self.commands.aliases[theCommand](
                    self, message, message.content.replace(F"+{theCommand} ", '')))
            # await message.delete()
        elif message.content.endswith('?'):
            print(message.content)
            if self.config['k']:
                await message.channel.send(f"> {message.content}\nK")

    async def setStatus(self, newStatus):
        await self.change_presence(activity=discord.Game(newStatus))

    async def close(self):
        open(Configfile, 'w').write(json.dumps(self.config, indent=2))
        await discord.Client.close(self)

    def isAuthed(self, user):
        if user in self.config['authedUsers']:
            return True
        else:
            return False
