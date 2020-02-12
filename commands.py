import datetime
import asyncio


class Commands():

    def __init__(self):
        self.aliases = {
            'now': self.now,
            'help': self.help,
            'send': self.send,
            'stop': self.stop,
            'restart': self.restart,
            'dsend': self.dSend,
            'setstatus': self.status,
            'auth': self.authUser,
            'deauth': self.deAuthUser,
            'listauthed': self.listAuthedUsers,
            'nuke': self.massDelete
        }
    
    async def massDelete(self, client, msg, txt):
        await msg.delete()
        if client.isAuthed(msg.author.id):
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

    async def authUser(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            target = msg.mentions[0]
            client.config['authedUsers'].append(target.id)
            await msg.channel.send(f'`Authed {target.name}#{target.discriminator}`')

    async def listAuthedUsers(self, client, msg, txt):
        users = ''
        for user in client.config['authedUsers']:
            theUser = await client.fetch_user(user)
            users += f"`{theUser.name}#{str(theUser.discriminator)}` "
        await msg.channel.send(users)

    async def status(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await client.setStatus(txt)

    async def stop(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await msg.channel.send('```❌ Bot has been stopped```')
            await client.close()

    async def restart(self, client, msg, txt):
        if client.isAuthed(msg.author.id):
            await msg.channel.send('```❌ Bot has been restarted```')
            client.restart = True
            await client.close()

    async def dSend(self, client, msg, txt):
        split = str.split(txt)
        token = split[0]
        time = split[1]
        channel = await client.fetch_channel(token)
        txt = txt.replace(f'{token} ','')
        txt = txt.replace(f'{time} ','')
        time = datetime.time.fromisoformat(time)
        time = datetime.datetime.combine(datetime.date.today(),time)
        difference = time - datetime.datetime.now()
        print(difference)
        await asyncio.sleep(difference.total_seconds())
        await channel.send(txt)
        await msg.channel.send(F'Sent message in <#{token}>')

    async def send(self, client, msg, txt):
        print(txt)
        token = str.split(txt)[0]
        channel = await client.fetch_channel(token)
        theContent = txt.replace(f'{token} ','')
        theContent = await self.swapBrackets(theContent)
        await channel.send(theContent)
        await msg.channel.send(F'Sent message in <#{token}>')

    async def now(self, client, msg, txt):
        await msg.channel.send(F'```{datetime.datetime.today()}```')

    async def swapBrackets(self, text):
        result = text.replace('[','<')
        result = result.replace(']','>')
        return result

    async def help(self, client, msg, txt):
        await msg.channel.send("""```Help for bot functions:


+help > This message

+now > Time in python format

+send [channel id] [message] > Sends message in channel with id provided

+dsend [channel id] [time] [message] > Delayed version of +send

+setstatus [status] > Sets bot status 🔒

+savelink > saves link to name provided

+(de)auth > allow a user to use locked commands 🔒

+listauthed > Lists authed users

+stop > stops the bot 🔒

+dm > dms a user, not to be abused 🔒

Note: some commands may not be available yet

```""")
