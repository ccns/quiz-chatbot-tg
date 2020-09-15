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
        message['correct'].append('👍' + provoke['message'])
    else:
        message['incorrect'].append('👎' + provoke['message'])

def reply_msg(condition):
    return message[condition][randrange(len(message[condition]))]

def judge_msg(correct):
    return reply_msg('correct') if correct else reply_msg('incorrect')

def prob_markup(prob_id, hint=False):
    keyboard = [[InlineKeyboardButton('A', callback_data=f'0 {prob_id}'),
                 InlineKeyboardButton('B', callback_data=f'1 {prob_id}'),
                 InlineKeyboardButton('C', callback_data=f'2 {prob_id}'),
                 InlineKeyboardButton('D', callback_data=f'3 {prob_id}')]]
    if hint:
        keyboard.append([
            InlineKeyboardButton('Hint', callback_data=f'hint {prob_id}')])

    return InlineKeyboardMarkup(keyboard)
