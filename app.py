#!/usr/bin/env python3
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import shuffle
import requests
from reply import Reply, Judge


def Reply_markup(have_hint):
    keyboard = [[InlineKeyboardButton('A', callback_data='0'),
                 InlineKeyboardButton('B', callback_data='1'),
                 InlineKeyboardButton('C', callback_data='2'),
                 InlineKeyboardButton('D', callback_data='3')]]
    if have_hint:
        keyboard.append([InlineKeyboardButton('Hint', callback_data='hint')])

    return InlineKeyboardMarkup(keyboard)


def Randomize_option(uid):
    global option_mapping
    option_mapping[uid] = [0, 1, 2, 3]
    shuffle(option_mapping[uid])


def Send_new_problem(bot, chat_id, uid):
    global entity
    entity[uid] = requests.get(url+'/question?user='+uid).json()
    Randomize_option(uid)
    op = entity[uid]['option']

    entity[uid]['question'] = '[' + entity[uid]['category'] + ']\n' + entity[uid]['question']
    for i in range(len(op)):
        entity[uid]['question'] += '\n(' + chr(ord('A')+i) + ') ' + op[option_mapping[uid][i]]

    entity[uid]['msg'] = bot.send_message(chat_id=chat_id, text=entity[uid]['question'],
                                          reply_markup=Reply_markup(have_hint=(entity[uid]['hint'] != '')))


def Finish(uid):
    stat = requests.get(url+'/user?user='+uid).json()
    total = len(stat['questionStatus'])

    if stat['questionStatus'].count(2) == total:
        return Reply('allpass')
    elif stat['questionStatus'].count(1) == total:
        return Reply('allwrong')

    return Reply('finish')


def Start(bot, update):
    global entity
    chat_id = update.message.chat_id
    uid = str(chat_id)

    if uid in entity:
        bot.edit_message_text(chat_id=chat_id, message_id=entity[uid]['msg'].message_id, text=entity[uid]['question'])

    status = requests.post(url+'/user', json={
        'user': uid,
        'nickname': update.message.from_user.first_name,
        'platform': 'telegram'
    }).status_code

    if status == 200:
        bot.send_message(chat_id=chat_id, text=Reply('welcome'))

    Send_new_problem(bot, chat_id, uid)


def Receive_and_reply(bot, update):
    rcv = update.callback_query
    chat_id = rcv.message.chat_id
    message_id = rcv.message.message_id
    uid = str(chat_id)
    om = option_mapping[uid]

    if rcv.data == 'hint':
        reply = entity[uid]['question'] + '\nHint:\n' + entity[uid]['hint']
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=reply,
                              reply_markup=Reply_markup(have_hint=False))
    else:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=entity[uid]['question'])

        result = requests.post(url+'/answer', json={'user': uid, 'id': entity[uid]['id'], 'answer': om[int(rcv.data)]}).json()
        bot.send_message(chat_id=chat_id, text=entity[uid]['option'][om[int(rcv.data)]])
        bot.send_message(chat_id=chat_id, text=Judge(result))
        if id == 'finish': bot.send_message(chat_id=chat_id, text=Finish(uid))
        Send_new_problem(bot, chat_id, uid)


def Status(bot, update):
    chat_id = update.message.chat_id
    uid = str(chat_id)

    stat = requests.get(url+'/user?user='+uid).json()
    remainders = stat['questionStatus'].count(0)
    reply = 'Score: ' + str(stat['point']) + '\nRank: ' + str(stat['order'])
    if remainders > 0:
        reply += '\nRemainders: ' + str(remainders)
    else:
        reply += '\nGame Completed!'

    bot.send_message(chat_id=chat_id, text=reply)


def Leaderboard(bot, update):
    reply = 'http://leaderboard.ccns.ncku.edu.tw'
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def Feedback(bot, update):
    reply = 'Submit a new issue:\nhttps://github.com/ccns/quiz-chatbot-tg/issues\nor contact us:\nhttps://www.facebook.com/ncku.ccns'
    bot.send_message(chat_id=update.message.chat_id, text=reply, disable_web_page_preview=True)


def main():
    global entity, option_mapping, url

    entity = {}
    option_mapping = {}

    url = '<url>'
    updater = Updater(token='<token>')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CallbackQueryHandler(Receive_and_reply))
    dispatcher.add_handler(CommandHandler('start', Start))
    dispatcher.add_handler(CommandHandler('status', Status))
    dispatcher.add_handler(CommandHandler('leaderboard', Leaderboard))
    dispatcher.add_handler(CommandHandler('feedback', Feedback))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
