import datetime
import asyncio
import re


class Scrape():
    def __init__(self, client):
        self.client = client
        self.theCommands = {
            'getjson': {'method': self.getJson, 'requiresAuth': True},
            'getPercentage' : {'method': self.getPercentage, 'requiresAuth': False}
        }
        self.client.addCommands(self.theCommands)

    async def getPercentage (self,msg,txt):
        async with msg.channel.typing():
            fullTotal = -1
            theTime = datetime.datetime.today()
            members = {}
            messageCount = {}
            async for message in msg.channel.history(limit=None):
                if not message.author.id in members:
                    members[message.author.id] = message.author.display_name
                    messageCount[message.author.id] = 1
                else:
                    messageCount[message.author.id] += 1
                fullTotal += 1
            output = f'```Total Messages in {msg.channel.name} - {fullTotal}\n'
            def by_value(item):
                return item[1]
            for key, value in sorted(messageCount.items(), key=by_value, reverse=True):
                output += f'{members[key]} - {value} messages {round(value/fullTotal*100,1)}%\n'
            output += "```"
        await msg.channel.send(output)

    async def getJson(self, msg, txt):
        fullTotal = 0
        counter = 0
        theTime = datetime.datetime.today()
        output = {
            'channelName': msg.channel.name,
            'timeSaved': theTime.__str__(),
            'exportUser': self.client.user.id,
            'members': {},
            'messages': []
        }
        theBefore = None
        await msg.delete()
        async for message in msg.channel.history(limit=None):
            if not message.author.id in output['members']:
                output['members'][message.author.id] = message.author.display_name
            theAttachments = []
            for attachment in message.attachments:
                theAttachments.append(attachment.url)
            output['messages'].append({'id': str(message.id), 'author': str(
                message.author.id), 'attachments': theAttachments, 'createdAt': message.created_at.__str__(), 'txt': message.content})
            fullTotal += 1
        output['messages'].reverse()
        print(fullTotal)
        if txt.find("-send") >= 0:
            await self.client.pushFile(msg.channel, output)
        else:
            theTime = theTime.isoformat().replace(
                ':', '_').replace('.', '_').replace(' ', '_')
            self.client.saveFile(output, f'{msg.channel.name}_{theTime}')
