import datetime
import asyncio
import re


class Scrape():
    def __init__(self, client):
        self.client = client
        self.theCommands = {
            'getjson': {'method': self.getJson, 'requiresAuth': True}
        }
        self.client.addCommands(self.theCommands)

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
        iterate = True
        while iterate:
            async for message in msg.channel.history(before=theBefore, limit=100):
                if not message.author.id in output['members']:
                    output['members'][message.author.id] = message.author.display_name
                theAttachments = []
                for attachment in message.attachments:
                    theAttachments.append(attachment.url)
                output['messages'].append({'id': str(message.id), 'author': str(
                    message.author.id), 'attachments': theAttachments, 'createdAt': message.created_at.__str__(), 'txt': message.content})
                fullTotal += 1
                counter += 1
                if counter == 100:
                    theBefore = message
            print(counter)
            if counter == 100:
                iterate = True
                counter = 0
            else:
                iterate = False
        output['messages'].reverse()
        print(fullTotal)
        if txt.find("-send") >= 0:
            await self.client.pushFile(msg.channel, output)
        else:
            theTime = theTime.isoformat().replace(
                ':', '_').replace('.', '_').replace(' ', '_')
            self.client.saveFile(output, f'{msg.channel.name}_{theTime}')
