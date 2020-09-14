# CCNS Quiz Bot - Telegram Client

## Usage
Install dependencies by pipenv
```
$ pipenv install
```

Fill in telegram bot token & [quiz-server](https://github.com/ccns/quiz-server) host ip to `.env`
```
$ cp .env.example .env
$ vim .env
```

Start the bot
```
$ pipenv run ./app.py
```

## Reference
https://core.telegram.org/bots

https://github.com/python-telegram-bot/python-telegram-bot
