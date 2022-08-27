from dotenv import dotenv_values
import asyncio
from telethon import TelegramClient, events

config = dotenv_values('.env')

bot_token = config['BOT_TOKEN']
api_id = int(config['API_ID'])
api_hash = config['API_HASH']

bot = TelegramClient('bot', api_id, api_hash)


@bot.on(events.NewMessage)
async def test_event_handler(event):
    if 'hello' in event.raw_text:
        await event.reply('hi!')


@bot.on(events.NewMessage)
async def get_file_size_handler(event):
    

with bot:
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()


