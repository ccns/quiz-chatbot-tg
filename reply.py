# reply.py
from random import randrange
import json

message = json.load(open('./messages.json'))


def Reply(condition):
    return message[condition][randrange(len(message[condition]))]


def Judge(bool):
    return ('👍 ' + Reply('correct')) if bool else ('👎 ' + Reply('incorrect'))
