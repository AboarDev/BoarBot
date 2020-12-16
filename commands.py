import datetime
import asyncio
import re


class Commands():

    def __init__(self, client):
        self.client = client
        self.theCommands = {
            'now': {'method': self.now, 'requiresAuth': False},
            'help': {'method': self.help, 'requiresAuth': False},
            'listauthedusers': {'method': self.listAuthedUsers, 'requiresAuth': False},

            'send': {'method': self.send, 'requiresAuth': True},
            'stop': {'method': self.stop, 'requiresAuth': True},
            'restart': {'method': self.restart, 'requiresAuth': True},
            'dsend': {'method': self.dSend, 'requiresAuth': True},
            'setstatus': {'method': self.status, 'requiresAuth': True},
            'authuser': {'method': self.authUser, 'requiresAuth': True},
            'deauthuser': {'method': self.deAuthUser, 'requiresAuth': True},
            'massdelete': {'method': self.massDelete, 'requiresAuth': True},

            'savedlink': {'method': self.savedLink, 'requiresAuth': False},
            'savelink': {'method': self.saveLink, 'requiresAuth': False},
            'savedlinks': {'method': self.savedLinks, 'requiresAuth': False},
            'emojiinfo': {'method': self.emojiInfo, 'requiresAuth': False},
            'listmembers': {'method': self.listMembers, 'requiresAuth': True},
            'repeatemoji': {'method': self.gems, 'requiresAuth': False},

            'rank': {'method': self.getRank, 'requiresAuth': False},
            'about': {'method': self.about, 'requiresAuth': False},
            'leaderboard': {'method': self.getLeaderBoard, 'requiresAuth': False}
        }
        #self.theUsers = users
        self.client.addCommands(self.theCommands)

    async def gems(self, msg, txt):
        split = txt.split(' ')
        theEmoji = split[0]
        NumberOfEmojis = 1
        if NumberOfEmojis > 3000:
            await msg.channel.send("Limit of 3000 emojis")
            return
        if len(split) > 1:
            NumberOfEmojis = split[1]
            NumberOfEmojis = NumberOfEmojis.lstrip()
            NumberOfEmojis = int(NumberOfEmojis)
        if re.match(r'<:.*([0-9])>', theEmoji):
            theEmoji = re.sub(r'[A-Za-z]+', '_', theEmoji)
        elif re.match(r'[0-9]+', theEmoji):
            theEmoji = self.client.get_emoji(int(theEmoji))
            if theEmoji:
                theEmoji = re.sub(r'[A-Za-z]+', '_', theEmoji.__str__())
            else:
                return
        theLength = len(theEmoji)
        maxEmojis = 2000//theLength
        print(maxEmojis)
        while NumberOfEmojis > 0:
            if NumberOfEmojis > maxEmojis:
                toSend = maxEmojis
            else:
                toSend = NumberOfEmojis
            await msg.channel.send(f'{theEmoji*toSend}')
            NumberOfEmojis -= toSend

    async def getRank(self, msg, txt):
        async with msg.channel.typing():
            theUsers = self.theUsers.outputUsers()
            count = 0
            for aUser in theUsers:
                count += 1
                if msg.author.id == aUser["id"] and ((aUser["exp"] != 0) or (aUser["level"] != 0)):
                    break
        await msg.channel.send(f'```{msg.author.name} Rank: {count} ```')

    async def about(self, msg, txt):
        theUser = self.theUsers.getUser(msg.author.id)
        await msg.channel.send(f'```{msg.author.name}\nLevel: {theUser.level}\nExp: {theUser.exp}\nCoins: {theUser.coins}```')

    async def getLeaderBoard(self, msg, txt):
        async with msg.channel.typing():
            output = ""
            theMembers = msg.guild.members
            theUsers = self.theUsers.outputUsers()
            theCount = 0
            for aUser in theUsers:
                theCount += 1
                nameObj = None
                for aMember in theMembers:
                    if aMember.id == aUser["id"]:
                        nameObj = aMember.display_name
                if nameObj == None:
                    nameObj = await self.client.fetch_user(aUser["id"])
                    nameObj = nameObj.name
                if aUser["level"] > 0 or aUser["exp"] > 0:
                    output += f'{theCount:02}. {nameObj} - Level: {aUser["level"]} Exp: {aUser["exp"]}\n'
        await msg.channel.send(f'```{output}```')

    async def listMembers(self, msg, txt):
        output = []
        for member in msg.guild.members:
            if member.bot == False:
                output.append(member.id)
        self.client.saveFile(output, f'{msg.guild.name}_users')

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

    async def emojiInfo(self, msg, txt):
        async with msg.channel.typing():
            toSend = ''
            txt = txt.replace(' ', '')
            theId = re.search(r'[0-9]{18}', txt)
            if theId:
                txt = theId[0]
            try:
                print(len(txt))
                emojiInt = int(txt)
                emoji = self.client.get_emoji(emojiInt)
                print(emoji, '/', txt)
                toSend = f'Type: Discord Emoji\nID: {emoji.id}\nName: {emoji.name}\nUsable by bot: {emoji.is_usable()}\nUrl: {emoji.url}\nRoles: {emoji.roles}'
            except ValueError:
                print(txt)
                toSend = f'Type: Unicode Emoji\nNative Format: `{txt}`'
        await msg.channel.send(toSend)

    async def saveLink(self, msg, txt):
        txt = txt.split()
        if 'http' in txt[1]:
            theLinks = self.client.config['savedLinks']
            if txt[0] not in theLinks:
                theLinks[txt[0]] = txt[1]
                await msg.channel.send(f"Saved link: `{txt[0]}`")

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
            await self.savedLinks(client, msg, txt)

    async def massDelete(self, msg, txt):
        await msg.delete()
        channel = msg.channel
        deleted = await channel.purge(limit=int(txt))
        await channel.send(F'```🗑 Deleted {len(deleted)} messages!```')

    async def deAuthUser(self, msg, txt):
        target = msg.mentions[0]
        self.client.config['authedUsers'].remove(target.id)
        await msg.channel.send(f'`DeAuthed {target.name}#{target.discriminator}`')

    async def authUser(self, msg, txt):
        target = msg.mentions[0]
        self.client.config['authedUsers'].append(target.id)
        await msg.channel.send(f'`Authed {target.name}#{target.discriminator}`')

    async def listAuthedUsers(self, msg, txt):
        users = ''
        for user in self.client.config['authedUsers']:
            theUser = await self.client.fetch_user(user)
            users += f"`{theUser.name}#{str(theUser.discriminator)}` "
        await msg.channel.send(users)

    async def status(self, msg, txt):
        await client.setStatus(txt)

    async def stop(self, msg, txt):
        await msg.channel.send('```❌ Bot has been stopped```')
        await client.close()

    async def restart(self, msg, txt):
        await msg.channel.send('```❌ Bot has been restarted```')
        client.restart = True
        await client.close()

    async def dSend(self, msg, txt):
        split = str.split(txt)
        token = split[0]
        time = split[1]
        channel = await self.client.fetch_channel(token)
        txt = txt.replace(f'{token} ', '')
        txt = txt.replace(f'{time} ', '')
        time = datetime.time.fromisoformat(time)
        time = datetime.datetime.combine(datetime.date.today(), time)
        difference = time - datetime.datetime.now()
        print(difference)
        await asyncio.sleep(difference.total_seconds())
        await channel.send(txt)
        await msg.channel.send(F'Sent message in <#{token}>')

    async def send(self, msg, txt):
        token = str.split(txt)[0]
        channel = await client.fetch_channel(token)
        theContent = txt.replace(f'{token} ', '')
        theContent = await self.swapBrackets(theContent)
        print(theContent)
        await channel.send(theContent)
        await msg.channel.send(F'Sent message in <#{token}>')

    async def now(self, msg, txt):
        await msg.channel.send(F'```{datetime.datetime.today()}```')

    async def swapBrackets(self, text):
        result = text.replace('[', '<')
        result = result.replace(']', '>')
        return result

    async def help(self, msg, txt):
        await msg.channel.send("""```Help for bot functions:\n
+help > This message\n
+now > Time in python format\n
+send [channel id] [message] > Sends message in channel with id provided\n
+dsend [channel id] [time] [message] > Delayed version of +send\n
+setstatus [status] > Sets bot status 🔒\n
+savelink [name] [link] > saves link to name provided\n
+savedlink [name] > gets saved link\n
+(de)authuser > allow a user to use locked commands 🔒\n
+listauthedusers > Lists authed users\n
+stop > stops the bot 🔒\n
+restart > restarts the bot 🔒\n
+massdelete [number of messages to delete] > deletes multiple messages 🔒\n
+getjson > [-send to send in chat] gets json of channel 🔒\n
+repeatemoji > [emoji] [number of times]\n
```""")
