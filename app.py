from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
from telegram import ReplyKeyboardMarkup
import requests
from reply import Reply, Judge


class charFilter(BaseFilter):
    def filter(self, message):
        return len(message.text) == 1 and message.text in ['0', '1', '2', '3']

entry = {}
keyboard = [['0', '1'], ['2', '3']]
url = '<url>'
updater = Updater(token='<token>')
dispatcher = updater.dispatcher
charfilter = charFilter()


def Reply_markup():
    return ReplyKeyboardMarkup(keyboard)


def Generate_problem(username):
    global entry
    entry[username] = requests.get(url+'/question?user='+username).json()
    prob = entry[username]['question']
    op = entry[username]['option']

    for i in range(len(op)):
        prob = prob + '\n(' + str(i) + ') ' + op[i]
    return prob


def Start(bot, update):
    username = str(update.message.chat_id)

    requests.post(url+'/user', json={"user": username})
    bot.send_message(chat_id=update.message.chat_id, text=Reply('welcome'), reply_markup=Reply_markup())
    bot.send_message(chat_id=update.message.chat_id, text=Generate_problem(username))


def Receive_and_reply(bot, update):
    username = str(update.message.chat_id)
    rcv = update.message.text
    op = entry[username]['option']
    id = entry[username]['id']

    result = requests.post(url+'/answer', json={'user': username, 'id': id, 'answer': int(rcv)}).json()
    bot.send_message(chat_id=update.message.chat_id, text=op[int(rcv)])
    bot.send_message(chat_id=update.message.chat_id, text=Judge(result))
    bot.send_message(chat_id=update.message.chat_id, text=Generate_problem(username))


def Status(bot, update):
    username = str(update.message.chat_id)
    stat = requests.get(url+'/user?user='+username).json()
    reply = 'Score: ' + str(stat['point']) + '\nRank: ' + str(stat['order']) + '\nRemainders: ' + str(stat['questionStatus'].count(0))

    bot.send_message(chat_id=update.message.chat_id, text=reply)


dispatcher.add_handler(MessageHandler(charfilter, Receive_and_reply))
dispatcher.add_handler(CommandHandler('start', Start))
dispatcher.add_handler(CommandHandler('status', Status))

updater.start_polling()
updater.idle()
