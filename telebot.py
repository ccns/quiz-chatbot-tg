from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import requests

entry = {}
username = ''
keyboard = [['0', '1'], ['2', '3']]
url = '<URL>'
updater = Updater(token='<TOKEN>')
dispatcher = updater.dispatcher


def generate_problem():
    global entry
    entry = requests.get(url+'/question?user='+username).json()
    prob = entry['question'] + '\n'
    for i in range(4):
        prob = prob + '(' + str(i) + ') ' + entry['option'][i] + '\n'
    return prob


def reply_markup():
    return ReplyKeyboardMarkup(keyboard)


def start(bot, update):
    global username
    username = str(update.message.chat_id)
    print(username)
    requests.post(url+'/user', json={"user": username})
    hello = "Hello " + update.message.from_user.first_name + ", nice to meet you!"
    bot.send_message(chat_id=update.message.chat_id, text=hello,
                     reply_markup=reply_markup())
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem())


def reply(ok):
    if ok:
        return "yes"
    else:
        return "no"


def reply_and_new_prob(bot, update):
    res = update.message.text
    op = entry['option']
    id = entry['id']
    bot.send_message(chat_id=update.message.chat_id, text=op[int(res)])
    result = requests.post(url+'/answer', json={'user': username, 'id': id, 'answer': int(res)}).json()
    bot.send_message(chat_id=update.message.chat_id, text=reply(result))
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem())


dispatcher.add_handler(MessageHandler(Filters.text, reply_and_new_prob))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()
