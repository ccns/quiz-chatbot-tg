import json
from pathlib import Path
from random import randrange

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from . import backend

path = Path(__file__).parent / 'messages.json'
message = json.load(path.open())
provokes = backend.get_provokes()

for provoke in provokes['data']:
    if provoke['correct']:
        message['correct'].append(provoke['message'])
    else:
        message['incorrect'].append(provoke['message'])

def reply_msg(condition):
    return message[condition][randrange(len(message[condition]))]

def judge_msg(correct):
    return reply_msg('correct') if correct else reply_msg('incorrect')

def prob_markup(hint):
    keyboard = [[InlineKeyboardButton('A', callback_data='0'),
                 InlineKeyboardButton('B', callback_data='1'),
                 InlineKeyboardButton('C', callback_data='2'),
                 InlineKeyboardButton('D', callback_data='3')]]
    if hint:
        keyboard.append([InlineKeyboardButton('Hint', callback_data='hint')])

    return InlineKeyboardMarkup(keyboard)
