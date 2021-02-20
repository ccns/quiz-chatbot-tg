#!/usr/bin/env python3
import logging
from typing import Dict

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
from bot.reply import reply_msg, judge_msg, prob_markup
from bot.user import User
from bot.config import TOKEN

request = telegram.utils.request.Request(con_pool_size=20)
bot = telegram.Bot(token=TOKEN, request=request)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
ENTITY: Dict[str, User] = {}

def send_new_problem(chat_id):
    global ENTITY
    uid = str(chat_id)
    prob = ENTITY[uid].get_problem()

    if prob:
        bot.send_message(
            chat_id=chat_id,
            text=prob.text(),
            parse_mode='HTML',
            reply_markup=prob_markup(prob.quiz_uuid, hint=prob.hint)
        )
    else:
        bot.send_message(chat_id=chat_id, text=reply_msg('finish'))
        bot.send_message(
            chat_id=chat_id,
            text='你已完成所有題目！\n若是想繼續練習可以輸入 /start 繼續作答(不計分)'
        )

def start_handler(update, _):
    global ENTITY
    chat_id = update.message.chat_id
    uid = str(chat_id)
    nickname = update.message.from_user.username

    if uid in ENTITY:
        send_new_problem(chat_id)
    else:
        user = User(nickname)
        if not user.register():
            reply = '無法建立帳號，請於粉專或 discord 私訊小編！'
            bot.send_message(chat_id=chat_id, text=reply)
            return

        logger.info(f'User {nickname}({uid}) registered')
        ENTITY[uid] = user
        bot.send_message(chat_id=chat_id, text=reply_msg('welcome'))
        send_new_problem(chat_id)

def callback_handler(update, _):
    global ENTITY
    ans, quiz_uuid = update.callback_query.data.split(' ')
    msg = update.callback_query.message
    uid = str(msg.chat_id)

    if uid not in ENTITY:
        return

    user = ENTITY[uid]

    # ignore any intend to answer old problems
    if quiz_uuid != user.prob.quiz_uuid:
        update.callback_query.answer()
        return

    if ans == '__HINT__':
        bot.edit_message_reply_markup(
            chat_id=msg.chat_id,
            message_id=msg.message_id,
            reply_markup=prob_markup(quiz_uuid)
        )
        reply = f'Hint: {ENTITY[uid].prob.hint}'
        bot.send_message(chat_id=msg.chat_id, text=reply)
    else:
        bot.edit_message_reply_markup(
            chat_id=msg.chat_id,
            message_id=msg.message_id
        )
        result = user.check_answer(ans)
        bot.send_message(chat_id=msg.chat_id, text=judge_msg(result))
        send_new_problem(msg.chat_id)

def status_handler(update, _):
    global ENTITY
    chat_id = update.message.chat_id
    uid = str(chat_id)

    if uid not in ENTITY:
        reply = '出錯啦，嘗試重新輸入 /start 看看'
        bot.send_message(chat_id=chat_id, text=reply)
        return

    user = ENTITY[uid]
    stat = user.get_status()
    remain = stat['no_answer_count']
    score = stat['score']
    rank = stat['rank']
    reply = f"得分: {score}\n排名: 第 {rank} 名\n"

    if remain > 0:
        reply += f'剩餘題數: {remain} 題'
    else:
        reply += 'Game Completed!'

    bot.send_message(chat_id=chat_id, text=reply)

def leaderboard_handler(update, _):
    reply = 'https://leaderboard.ccns.io'
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def feedback_handler(update, _):
    reply = '''Submit a new issue:
https://github.com/ccns/quiz-chatbot-tg/issues
or contact us:
https://www.facebook.com/ncku.ccns'''

    bot.send_message(
        chat_id=update.message.chat_id,
        text=reply
    )

def error_handler(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(callback_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('start', start_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('status', status_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('leaderboard', leaderboard_handler, run_async=True))
    dispatcher.add_handler(CommandHandler('feedback', feedback_handler, run_async=True))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
