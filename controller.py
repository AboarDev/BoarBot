import asyncio
import bot
from scrape import Scrape
from userlevels import UserLevels
from commands import Commands
from importlib import reload

Token = open('token.txt').read()


def runBot():
    loop = asyncio.get_event_loop()
    theClient = bot.BotClient()
    commands = Commands(theClient)
    levels = UserLevels(theClient)
    scrape = Scrape(theClient)
    try:
        loop.run_until_complete(theClient.start(Token))
    except KeyboardInterrupt:
        loop.run_until_complete(theClient.close())
    finally:
        loop.close()

    if theClient.restart == True:
        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
        reload(bot)
        runBot()


runBot()
