from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
from telegram import ReplyKeyboardMarkup
import requests
class charFilter(BaseFilter):
    def filter(self, message):
        return len(message.text) == 1 and message.text in ['0','1','2','3']

entry = {}
keyboard = [['0', '1'], ['2', '3']]
url = '<url>'
updater = Updater(token='<token>')
dispatcher = updater.dispatcher
charfilter = charFilter()


def generate_problem(username):
    global entry
    entry[username] = requests.get(url+'/question?user='+username).json()
    prob = entry[username]['question'] + '\n'
    for i in range(4):
        prob = prob + '(' + str(i) + ') ' + entry[username]['option'][i] + '\n'
    return prob


def reply_markup():
    return ReplyKeyboardMarkup(keyboard)


def start(bot, update):
    username = str(update.message.chat_id)
    hello = "Hello " + update.message.from_user.first_name + ", nice to meet you!"

    requests.post(url+'/user', json={"user": username})
    bot.send_message(chat_id=update.message.chat_id, text=hello, reply_markup=reply_markup())
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem(username))


def reply(ok):
    if ok:
        return "すごーい!"
    else:
        return "是不會查 stackoverflow 嗎？ㄏㄏ"


def reply_and_new_prob(bot, update):
    username = str(update.message.chat_id)
    res = update.message.text
    op = entry[username]['option']
    id = entry[username]['id']

    result = requests.post(url+'/answer', json={'user': username, 'id': id, 'answer': int(res)}).json()
    bot.send_message(chat_id=update.message.chat_id, text=op[int(res)])
    bot.send_message(chat_id=update.message.chat_id, text=reply(result))
    bot.send_message(chat_id=update.message.chat_id, text=generate_problem(username))


dispatcher.add_handler(MessageHandler(charfilter, reply_and_new_prob))
dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()
