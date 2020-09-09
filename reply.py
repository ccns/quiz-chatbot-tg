from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import randrange
import json

message = json.load(open('./messages.json'))

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