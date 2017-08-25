from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
from telegram import ReplyKeyboardMarkup
import requests
from reply import Reply, judge


class charFilter(BaseFilter):
    def filter(self, message):
        return len(message.text) == 1 and message.text in ['0', '1', '2', '3']

entry = {}
keyboard = [['0', '1'], ['2', '3']]
url = '<url>'
updater = Updater(token='<token>')
dispatcher = updater.dispatcher
charfilter = charFilter()


def reply_markup():
    return ReplyKeyboardMarkup(keyboard)


def generate_problem(username):
    global entry
    entry[username] = requests.get(url+'/question?user='+username).json()
    prob = entry[username]['question'] + '\n'
    for i in range(4):
        prob = prob + '(' + str(i) + ') ' + entry[username]['option'][i] + '\n'
    return prob


def start(bot, update):
    username = str(update.message.chat_id)

    requests.post(url+'/user', json={"user": username})
    bot.send_message(chat_id=update.message.chat_id, text=Reply('welcome'), reply_markup=reply_markup())
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem(username))


def receive_and_reply(bot, update):
    username = str(update.message.chat_id)
    res = update.message.text
    op = entry[username]['option']
    id = entry[username]['id']

    result = requests.post(url+'/answer', json={'user': username, 'id': id, 'answer': int(res)}).json()
    bot.send_message(chat_id=update.message.chat_id, text=op[int(res)])
    bot.send_message(chat_id=update.message.chat_id, text=judge(result))
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem(username))


dispatcher.add_handler(MessageHandler(charfilter, receive_and_reply))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()
