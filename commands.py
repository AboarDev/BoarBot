import datetime
import asyncio

class Commands():

    def __init__(self):
        self.theCommands = {
            'now': {'method': self.now, 'requiresAuth': False},
            'help': {'method': self.help, 'requiresAuth': False},
            'send': {'method': self.send, 'requiresAuth': True},
            'stop': {'method': self.stop, 'requiresAuth': True},
            'restart': {'method': self.restart, 'requiresAuth': True},
            'dsend': {'method': self.dSend, 'requiresAuth': True},
            'setstatus': {'method': self.status, 'requiresAuth': True},
            'authuser': {'method': self.authUser, 'requiresAuth': True},
            'deauthuser': {'method': self.deAuthUser, 'requiresAuth': True},
            'listauthedusers': {'method': self.listAuthedUsers, 'requiresAuth': False},
            'massdelete': {'method': self.massDelete, 'requiresAuth': True},
            'savedlink': {'method': self.savedLink, 'requiresAuth': False},
            'savelink': {'method': self.saveLink, 'requiresAuth': False},
            'savedlinks': {'method': self.savedLinks, 'requiresAuth': False},
            'emojiinfo': {'method': self.emojiInfo, 'requiresAuth': False},
            'getjson': {'method': self.getJson, 'requiresAuth': True},
            'listmembers': {'method': self.listMembers, 'requiresAuth': False}
        }

    async def listMembers(self, client, msg, txt):
        pass

    async def getJson(self, client, msg, txt):
        fullTotal = 0
        counter = 0
        theTime = datetime.datetime.today()
        output = {
            'channelName': msg.channel.name,
            'timeSaved': theTime.__str__(),
            'exportUser': client.user.id,
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
                output['messages'].append({'id': str(message.id), 'author':str(message.author.id), 'attachments': theAttachments, 'createdAt': message.created_at.__str__(), 'txt': message.content})
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
            await client.pushFile(msg.channel,output)
        else:
            theTime = theTime.isoformat().replace(':','_').replace('.','_').replace(' ','_')
            client.saveFile(output,f'{msg.channel.name}_{theTime}')

    async def emojiInfo(self, client, msg, txt):
        toSend = ''
        txt = txt.replace(' ','')
        try:
            emojiInt = int(txt)
            print(client.get_emoji(emojiInt),'/',txt)
            toSend = f'Type: Discord Emoji\nNative Format: `{client.get_emoji(int(txt))}`'
        except ValueError:
            print(txt)
            toSend = f'Type: Unicode Emoji\nNative Format: `{txt}`'
        await msg.channel.send(toSend)

    async def saveLink(self, client, msg, txt):
        txt = txt.split()
        if 'http' in txt[1]:
            theLinks = client.config['savedLinks']
            if theLinks[txt[0]] == False:
                theLinks[txt[0]] = txt[1]
                await msg.channel.send("```Link Saved```")

    async def savedLinks(self, client, msg, txt):
        theLinks = client.config['savedLinks']
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

    async def savedLink(self, client, msg, txt):
        theLinks = client.config['savedLinks']
        if txt in theLinks:
            await msg.channel.send(f'Saved link: {txt} | {theLinks[txt]}')
        else:
            await self.savedLinks(client, msg, txt)

    async def massDelete(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await msg.delete()
            channel = msg.channel
            deleted = await channel.purge(limit=int(txt))
            await channel.send(F'```🗑 Deleted {len(deleted)} messages!```')
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def deAuthUser(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            target = msg.mentions[0]
            client.config['authedUsers'].remove(target.id)
            await msg.channel.send(f'`DeAuthed {target.name}#{target.discriminator}`')
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def authUser(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            target = msg.mentions[0]
            client.config['authedUsers'].append(target.id)
            await msg.channel.send(f'`Authed {target.name}#{target.discriminator}`')
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def listAuthedUsers(self, client, msg, txt):
        users = ''
        for user in client.config['authedUsers']:
            theUser = await client.fetch_user(user)
            users += f"`{theUser.name}#{str(theUser.discriminator)}` "
        await msg.channel.send(users)

    async def status(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await client.setStatus(txt)
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def stop(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await msg.channel.send('```❌ Bot has been stopped```')
            await client.close()
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def restart(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await msg.channel.send('```❌ Bot has been restarted```')
            client.restart = True
            await client.close()
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def dSend(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            split = str.split(txt)
            token = split[0]
            time = split[1]
            channel = await client.fetch_channel(token)
            txt = txt.replace(f'{token} ', '')
            txt = txt.replace(f'{time} ', '')
            time = datetime.time.fromisoformat(time)
            time = datetime.datetime.combine(datetime.date.today(), time)
            difference = time - datetime.datetime.now()
            print(difference)
            await asyncio.sleep(difference.total_seconds())
            await channel.send(txt)
            await msg.channel.send(F'Sent message in <#{token}>')
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def send(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            token = str.split(txt)[0]
            channel = await client.fetch_channel(token)
            theContent = txt.replace(f'{token} ', '')
            theContent = await self.swapBrackets(theContent)
            await channel.send(theContent)
            await msg.channel.send(F'Sent message in <#{token}>')
        else:
            await msg.channel.send('🔒 Must be authed to use command')

    async def now(self, client, msg, txt):
        await msg.channel.send(F'```{datetime.datetime.today()}```')

    async def swapBrackets(self, text):
        result = text.replace('[', '<')
        result = result.replace(']', '>')
        return result

    async def help(self, client, msg, txt):
        await msg.channel.send("""```Help for bot functions:


+help > This message

+now > Time in python format

+send [channel id] [message] > Sends message in channel with id provided

+dsend [channel id] [time] [message] > Delayed version of +send

+setstatus [status] > Sets bot status 🔒

+savelink [name] [link] > saves link to name provided

+savedlink [name] > gets saved link

+(de)authuser > allow a user to use locked commands 🔒

+listauthedusers > Lists authed users

+stop > stops the bot 🔒

+restart > restarts the bot 🔒

+massdelete [number of messages to delete] > deletes multiple messages 🔒

+getjson > [-send to send in chat] gets json of channel 🔒

+dm > dms a user, not to be abused 🔒

```""")
