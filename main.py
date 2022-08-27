from dotenv import dotenv_values
import asyncio
from telethon import TelegramClient, events, functions
from telethon.utils import get_extension
from datetime import datetime
import os
import aiofiles
from aiocsv import AsyncReader


def get_current_time():
    now = datetime.now()

    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    return dt_string


async def parse_csv(path):
    async with aiofiles.open(path, mode="r", encoding="utf-8", newline = "") as afp:
        async for name in AsyncReader(afp):
            result = await bot(functions.account.CheckUsernameRequest(
                username=name[0]
            ))
            print(result)


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


#TODO: Add button handling for convinience
@bot.on(events.NewMessage(incoming=True, ))
async def parse_file(event):
    sender = await event.get_sender()
    sender = sender.username
    chat = await event.get_chat()

    date = get_current_time()
    file_path = f"./tmp/{sender}_{date}"

    extension = get_extension(event.document)

    if extension == '.csv':
        file_path += extension
        await bot.download_file(
            event.document,
            file_path
        )

        await bot.send_message(
            event.chat_id,
            f"Accepted your file at {file_path}"
        )

        await parse_csv(file_path)
    else:
        await bot.send_message(
            event.chat_id,
            "Wrong file format"
        )


with bot:
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()


