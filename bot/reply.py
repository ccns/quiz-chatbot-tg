from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import randrange
from pathlib import Path
from .backend import backend
import json

path = Path(__file__).parent / 'messages.json'
message = json.load(path.open())
provokes = backend.get_provokes()

for provoke in provokes['data']:
    if provoke['correct']:
        message['correct'].append(provoke['message'])
    else:
        message['incorrect'].append(provoke['message'])

def ReplyMsg(condition):
    return message[condition][randrange(len(message[condition]))]

def JudgeMsg(correct):
    return ReplyMsg('correct') if correct else ReplyMsg('incorrect')

def ProbMarkup(hint):
    keyboard = [[InlineKeyboardButton('A', callback_data='0'),
                 InlineKeyboardButton('B', callback_data='1'),
                 InlineKeyboardButton('C', callback_data='2'),
                 InlineKeyboardButton('D', callback_data='3')]]
    if hint:
        keyboard.append([InlineKeyboardButton('Hint', callback_data='hint')])

    return InlineKeyboardMarkup(keyboard)