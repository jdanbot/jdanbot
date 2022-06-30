<div align="center">
  <h1>🤖 jdan734-bot</h1>
  <a href="https://t.me/jdan734_bot" target="__blank"><img src="https://img.shields.io/badge/Telegram-Bot-blue.svg?logo=telegram"></a><br/>
  <h3>Multifunctional Telegram Bot for banning and stuff.</h3>
</div><br>

## 🚀 Start
To start, clone this repo and run this code:
```sh
pip install -r requirements.txt
poetry install
poetry run python -m bot
```

## ⚙️ Configuring
Fill in .secrets.toml token for [Telegram](t.me/BotFather) and other settings from [`config.py`](https://github.com/jDan735/jdan734-bot/blob/nightly/bot/config/config.py) if is need. For example:

```toml
status = "<custom bot status>"
logging_chat = -10012345678

[tokens]
bot_token = "12345678909:AVEFWGRGHTHHRGGERGEG"
```
