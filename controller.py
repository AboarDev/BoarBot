import asyncio
import bot
from importlib import reload

Token = open('F:/Pyth/BoarBot/token.txt').read()
def runBot():
  theClient = bot.BotClient()
  theClient.run(Token)
  print(theClient.restart)
  if asyncio.get_event_loop().is_closed():
    asyncio.set_event_loop(asyncio.new_event_loop())
  if theClient.restart == True:
    reload(bot)
    runBot()

runBot()