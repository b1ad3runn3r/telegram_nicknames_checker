from dotenv import dotenv_values
import asyncio
from telethon import TelegramClient, events


config = dotenv_values('.env')

bot_token = config['BOT_TOKEN']
api_id = int(config['API_ID'])
api_hash = config['API_HASH']

bot = TelegramClient('bot', api_id, api_hash)


@bot.on(events.NewMessage(incoming=True, pattern="/start"))
async def start(event):
    sender = await event.get_sender()
    msg = f"Hello, **{sender.username}**!\
            \nThis is a username checker bot.\
            \nPlease send me a **.csv** file and I will check."

    await event.reply(msg)


@bot.on(events.NewMessage(incoming=True, pattern="/help"))
async def bot_help(event):
    msg = f"/start - begin interaction with bot\
            \n/help - print this help message\
            \nHow to use this bot:\
            \nSend a **.csv** file and it will check the list of usernames for availability."

    await event.reply(msg)


with bot:
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()


