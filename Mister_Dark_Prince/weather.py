import asyncio
import os

import requests
from pyrogram import Client, filters
from pyrogram.types import Message

from config import HNDLR

from .darkprince.helpo import modules_help


def get_pic(city):
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=en.png", stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            pic.write(block)
        return file_name


@Client.on_message(filters.command("weather", prefixes=f"{HNDLR}") & filters.me)
async def weather(client: Client, message: Message):
    try:
        city = message.command[1]
        await message.edit("```Processing the request...```")
        r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        await message.edit(f"```City: {r.text}```")
        await client.send_document(
            chat_id=message.chat.id,
            document=get_pic(city),
            reply_to_message_id=message.message_id,
        )
        os.remove(f"{city}.png")
    except:
        await message.edit("<code>Error occured</code>")
        await asyncio.sleep(5)
        await message.delete()


modules_help.append(
    {
        "weather": [
            {"weather [city]*": "Get the weather in the selected city"},
        ]
    }
)
