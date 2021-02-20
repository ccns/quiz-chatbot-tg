import json
from pathlib import Path
from random import randrange

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from . import backend

path = Path(__file__).parent / 'messages.json'
message = json.load(path.open())
provokes = backend.get_provokes()

for provoke in provokes:
    if provoke['correct']:
        message['correct'].append('👍' + provoke['message'])
    else:
        message['incorrect'].append('👎' + provoke['message'])

def reply_msg(condition):
    return message[condition][randrange(len(message[condition]))]

def judge_msg(correct):
    return reply_msg('correct') if correct else reply_msg('incorrect')

def prob_markup(quiz_uuid, hint=False):
    keyboard = [[InlineKeyboardButton('A', callback_data=f'0 {quiz_uuid}'),
                 InlineKeyboardButton('B', callback_data=f'1 {quiz_uuid}'),
                 InlineKeyboardButton('C', callback_data=f'2 {quiz_uuid}'),
                 InlineKeyboardButton('D', callback_data=f'3 {quiz_uuid}')]]
    if hint:
        keyboard.append([
            InlineKeyboardButton('Hint', callback_data=f'__HINT__ {quiz_uuid}')])

    return InlineKeyboardMarkup(keyboard)