from dotenv import dotenv_values
import asyncio
from telethon import TelegramClient, events, functions, errors
from telethon.utils import get_extension
from datetime import datetime
import time
import os
import aiofiles
from aiocsv import AsyncReader, AsyncWriter
from enum import Enum, auto

config = dotenv_values('.env')

api_id = int(config['API_ID'])
api_hash = config['API_HASH']

bot = TelegramClient('anon', api_id, api_hash)


class State(Enum):
    WAIT_FILE = auto()


conversation_state = {}


def get_current_time():
    now = datetime.now()

    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    return dt_string


async def parse_csv(path):
    good_names = []
    cnt = 0
    async with aiofiles.open(path, mode="r", encoding="utf-8", newline="") as afp:
        async for name in AsyncReader(afp):
            cnt += 1
            try:
                result = await bot(functions.account.CheckUsernameRequest(
                    username=name[0]
                ))

                if result:
                    good_names.append(['@' + name[0]])

            except errors.FloodWaitError as fW:
                time.sleep(fW.seconds)

            except errors.UsernameInvalidError:
                continue

    saved_path = path.split('.')[0] + '_out.' + path.split('.')[1]

    async with aiofiles.open(saved_path, mode="w", encoding="utf-8", newline="") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        await writer.writerows(good_names)

    good_p = 100 * (len(good_names) / cnt)
    bad_p = 100 - good_p

    msg = 'Stats:\n' + f'Good:\t{good_p}%\n' + f'Bad:\t{bad_p}%'
    
    return msg, saved_path


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
            \nYou should send the bot a /test command and after it replies,\
            send a csv file that contains nicknames you want to check"

    await event.reply(msg)


@bot.on(events.NewMessage(incoming=True))
async def check_nicknames(event):

    date = get_current_time()
    file_path = f"tmp/{event.sender_id}_{date}"

    state = conversation_state.get(event.sender_id)

    if state is None:
        await event.respond('Hi! Please send a file')
        conversation_state[event.sender_id] = State.WAIT_FILE

    elif state == State.WAIT_FILE:
        await event.respond('Working...')
        extension = ''
        if event.document:
            extension = get_extension(event.document)
        else:
            await bot.send_message(
                event.chat_id,
                "Please send me a file"
            )

        # TODO: Finish handler if no file is sent

        if extension == '.csv' or extension == '.xls':
            file_path += '.csv'
            await bot.download_file(
                event.document,
                file_path
            )

            msg, saved_path = await parse_csv(file_path)
            await bot.send_file(
                event.chat_id,
                saved_path,
                caption=msg
            )

            os.remove(file_path)
            os.remove(saved_path)

        else:
            await bot.send_message(
                event.chat_id,
                "Wrong file format"
            )
            # TODO: Fix issues when sending file from iPhone

        del conversation_state[event.sender_id]


with bot:
    bot.start()
    bot.run_until_disconnected()
