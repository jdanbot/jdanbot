from .token import bot

@bot.message_handler(func=lambda message: message.forward_from == "Канал Максима Каца")
def pin_kaz(message):
    if isinstance(message.text, str):
        return

    do_pin = False

    for entity in message.text:
        if isinstance(entity, str):
            continue

        if "text" not in entity:
            continue

        if "youtu" in entity["text"]:
            do_pin = True

    if do_pin:
        bot.pinChatMessage(message.chat, message.message_id)

