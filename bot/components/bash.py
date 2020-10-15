"""
@bot.message_handler(commands=["bashorg"])
def bashorg(message):
    num = int(message.text.replace("/bashorg@jDan734_bot ", "").replace("/bashorg ", ""))
    r = requests.get(f"https://bash.im/quote/{num}")
    soup = BeautifulSoup(r.text.replace("<br>", "БАН").replace("<br\\>", "БАН"), 'html.parser')

    print(soup.find("div", class_="quote__body").text.replace('<div class="quote__body">', "").replace("</div>", "").replace("<br\\>", "\n"))

    soup2 = BeautifulSoup(soup.find("div", class_="quote__body"), "lxml")
    bot.reply_to(message, soup2)
"""
