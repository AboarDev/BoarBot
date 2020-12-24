import datetime
import asyncio
import re
import json
import random

Configfile = 'config/templates.json'

class Messages():

    def __init__(self, client):
        self.client = client
        self.theCommands = {
            'setMessages': {'method': self.setMessages, 'requiresAuth': True}
        }
        self.client.addCommands(self.theCommands)
        self.counter = 0
        self.client.addCommands(self.theCommands)
        self.client.addHandler(self.on_message)

        config = json.loads(open(Configfile).read())
        self.frequency = config["frequency"]
        self.templates = config["templates"]
        self.messageChannel = config["randomMessageChannel"]
        self.enabled = config["randomMessages"]
        self.P = config["P"]
        self.A = config["A"]
        self.X = config["X"]
        self.T = config["T"]

    def setMessages(self):
        self.enabled = not self.enabled

    def createMessage(self):
        template = random.choice(self.templates)
        message = template.replace("P",random.choice(self.P))
        message = message.replace("A",random.choice(self.A))
        message = message.replace("X",random.choice(self.X))
        message = message.replace("T",random.choice(self.T))
        return message

    async def on_message(self,msg):
        if self.enabled:
            self.counter += 1
            channel = await self.client.fetch_channel(self.messageChannel)
            if self.counter >= self.frequency:
                self.counter = 0
                message = self.createMessage()
                await channel.send(message)