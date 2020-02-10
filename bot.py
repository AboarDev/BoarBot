import discord
from commands import Commands
import asyncio
import datetime
import time
import json

Token = open('F:/Pyth/BoarBot/token.txt').read()
Configfile = 'F:/Pyth/BoarBot/config.json'


class BotClient(discord.Client):

    def __init__(self):
        discord.Client.__init__(self)
        self.commands = Commands()
        self.config = json.loads(open(Configfile).read())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=discord.Game('Alive, once more!'))

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

    async def shutDown(self):
        open(Configfile, 'w').write(json.dumps(self.config, indent=2))
        await self.close()

    def isAuthed(self, user):
        if user in self.config['authedUsers']:
            return True
        else:
            return False


client = BotClient()
client.run(Token)
