from .bot import bot, dp

import aiohttp
import json


async def getRules(page):
    url = f"https://api.telegra.ph/getPage/{page}"
    params = {"return_content": "true"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if not response.status == 200:
                return 404

            return json.loads(await response.text())["result"]


def page_to_text(page):
    text = f'<b>{page["title"]}</b>\n\n'

    for element in page["content"]:
        if "tag" in element["children"][0]:
            break

        text += element["children"][0]

        if element["tag"] == "p":
            text += "\n"

    return text


@dp.message_handler(commands=["rules"])
async def chat_rules(message, reply=True):
    rules = await getRules("Ustav-profsoyuza-Botov-Maksima-Kaca-08-15")
    text = page_to_text(rules)

    await bot.send_chat_action(message.chat.id, "typing")
    if reply:
        await message.reply(text, parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, text, parse_mode="HTML")
