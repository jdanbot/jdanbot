from .token import bot
import requests
import json


@bot.message_handler(commands=["github"])
def github(message):
    try:
        url = message.text.split(maxsplit=1)[1]

    except:
        bot.reply_to(message, "Введи название аккаунта")
        return

    try:
        r = requests.get(f"https://api.github.com/users/{url}")
        repos = requests.get(f"https://api.github.com/users/{url}/repos")
        data = json.loads(r.text)
        repos_list = json.loads(repos.text)
        text = f'*{data["name"]}*\nFollowers `{data["followers"]}` Following `{data["following"]}`\n\n__{data["bio"]}__\n\nRepositories:'

        for repo in repos_list:
            print(repo["full_name"])
            text += f'\n[{repo["full_name"]}]({repo["html_url"]})'

        bot.send_photo(message.chat.id,
                       data["avatar_url"],
                       caption=text,
                       parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, e)
