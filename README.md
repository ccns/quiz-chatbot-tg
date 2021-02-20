# CCNS Quiz Bot - Telegram Client

## Usage
Install dependencies by poetry
```
$ poetry install
```

Fill in telegram bot token & [quiz-server](https://github.com/ccns/quiz-server) host ip to `.env`
```
$ cp .env.example .env
$ vim .env
```

Start the bot
```
$ poetry run python3 app.py
```

## Reference
https://core.telegram.org/bots

https://github.com/python-telegram-bot/python-telegram-bot
