#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from bot.reply import ReplyMsg, JudgeMsg, ProbMarkup
from bot.user import User
import telegram
import logging
import configparser

config = configparser.ConfigParser()
config.read('.config')
TOKEN = config['Bot']['Token']

request = telegram.utils.request.Request(con_pool_size=20)
bot = telegram.Bot(token=TOKEN, request=request)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
entity = {}

def send_new_problem(chat_id):
    global entity

    uid = str(chat_id)
    prob = entity[uid].get_problem()

    if prob:
        bot.send_message(
            chat_id=chat_id,
            text=prob.text(),
            parse_mode='HTML',
            reply_markup=ProbMarkup(hint=prob.hint)
        )
    else:
        entity[uid].finished = True
        bot.send_message(chat_id=chat_id, text=ReplyMsg('finish'))

@run_async
def start_handler(update, context):
    chat_id = update.message.chat_id
    uid = str(chat_id)

    print({
        'user': uid,
        'nickname': update.message.from_user.first_name,
    })

    if uid in entity:
        send_new_problem(chat_id)
    else:
        user = User(uid)
        if not user.register():
            reply = 'Cannot register you as a player, please contact admin'
            bot.send_message(chat_id=chat_id, text=reply)
            return

        entity[uid] = user
        bot.send_message(chat_id=chat_id, text=ReplyMsg('welcome'))
        send_new_problem(chat_id)

@run_async
def callback_handler(update, context):
    ans = update.callback_query.data
    msg = update.callback_query.message
    uid = str(msg.chat_id)
    user = entity[uid]

    if ans == 'hint':
        bot.edit_message_reply_markup(
            chat_id=msg.chat_id,
            message_id=msg.message_id,
            reply_markup=ProbMarkup(hint=False)
        )
        reply = f'Hint: {entity[uid].prob.hint}'
        bot.send_message(chat_id=msg.chat_id, text=reply)
    else:
        bot.edit_message_reply_markup(
            chat_id=msg.chat_id,
            message_id=msg.message_id
        )
        result = user.check_answer(ans)
        bot.send_message(chat_id=msg.chat_id, text=JudgeMsg(result))
        send_new_problem(msg.chat_id)

@run_async
def status_handler(update, context):
    chat_id = update.message.chat_id
    uid = str(chat_id)

    if uid not in entity:
        reply = 'Something went wrong, please try enter /start again'
        bot.send_message(chat_id=chat_id, text=reply)
        return

    user = entity[uid]
    stat = user.get_status()
    remain = stat['remain']
    reply = f"Score: {stat['point']}\nRank: {stat['order']}\n"
    if remain > 0:
        reply += f'Remain: {remain} problems'
    else:
        reply += 'Game Completed!'

    bot.send_message(chat_id=chat_id, text=reply)

@run_async
def leaderboard_handler(update, context):
    reply = 'http://109-fall-leaderboard.ccns.io'
    bot.send_message(chat_id=update.message.chat_id, text=reply)

@run_async
def feedback_handler(update, context):
    reply = '''Submit a new issue:
https://github.com/ccns/quiz-chatbot-tg/issues
or contact us:
https://www.facebook.com/ncku.ccns'''

    bot.send_message(
        chat_id=update.message.chat_id,
        text=reply,
        disable_web_page_preview=True
    )

def error_handler(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    dispatcher.add_handler(CommandHandler('start', start_handler))
#    dispatcher.add_handler(CommandHandler('status', status_handler))
    dispatcher.add_handler(CommandHandler('leaderboard', leaderboard_handler))
    dispatcher.add_handler(CommandHandler('feedback', feedback_handler))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
