import asyncio
import re


class SaveLinks():

    def __init__(self, client):
        self.client = client
        self.theCommands = {
            'savedlink': {'method': self.savedLink, 'requiresAuth': False},
            'savelink': {'method': self.saveLink, 'requiresAuth': False},
            'savedlinks': {'method': self.savedLinks, 'requiresAuth': False},
            'removelink': {'method': self.removeLink, 'requiresAuth': True}
        }
        self.client.addCommands(self.theCommands)

    async def removeLink(self, msg, txt):
        txt = txt.split()
        theLinks = self.client.config['savedLinks']
        if txt[0] in theLinks:
            del theLinks[txt[0]]
    
    async def saveLink(self, msg, txt):
        txt = txt.split()
        if len(txt) > 1 and 'http' in txt[1]:
            theLinks = self.client.config['savedLinks']
            if txt[0] not in theLinks:
                theLinks[txt[0]] = txt[1]
                await msg.channel.send(f"Saved link: `{txt[0]}`")
                try:
                    await self.client.saveConfig()
                finally:
                    pass

    async def savedLinks(self, msg, txt):
        theLinks = self.client.config['savedLinks']
        count = 10
        linklist = []
        formattedLinks = ''
        for link in theLinks:
            formattedLink = f"{link}: {theLinks[link]}\n"
            if count + len(formattedLink) > 2000:
                linklist.append(formattedLinks)
                count = 10
                formattedLinks = ''
            formattedLinks += formattedLink
            count += len(formattedLink)
        linklist.append(formattedLinks)
        for link in linklist:
            await msg.channel.send(f"```{link}```")

    async def savedLink(self, msg, txt):
        theLinks = self.client.config['savedLinks']
        if txt in theLinks:
            await msg.channel.send(f'Saved link: `{txt}` | {theLinks[txt]}')
        else:
            await self.savedLinks(self.client, msg, txt)