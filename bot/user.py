from bot.request_type import AnswerReq, RegisterReq
from dataclasses import dataclass
from typing import List, Union
from random import shuffle

from . import backend

@dataclass
class Problem:
    quiz_uuid: str
    category: str
    question: str
    options: List[str]
    hint: Union[str, None] = None

    def text(self):
        quest = f'<b>[{self.category}]</b>\n{self.question.ljust(25, " ")}\n'

        for i in range(len(self.options)):
            opchar = chr(ord('A') + i)
            quest += f'({opchar}) {self.options[i]}\n'

        return quest

@dataclass
class User:
    username: str
    uuid: str = ''
    prob: Union[Problem, None] = None
    finished: bool = False

    def get_problem(self) -> Union[Problem, None]:
        if not self.finished:
            feed = backend.get_feed(self.uuid)
        else:
            feed = backend.get_rand_feed()

        if not feed:
            self.finished = True
            return

        self.prob = Problem(
            feed['quiz_uuid'],
            feed['domain'],
            feed['description'],
            feed['options'],
            None
        )
        return self.prob

    def check_answer(self, ans: str) -> bool:
        payload: AnswerReq = {
            'player_uuid': self.uuid,
            'quiz_uuid': self.prob.quiz_uuid,
            'answer': self.prob.options[int(ans)]
        }
        res = backend.post_answer(payload)
        return res['correct']

    def get_status(self):
        return backend.get_status(self.uuid)

    def register(self) -> bool:
        payload: RegisterReq = {
            'name': self.username,
            'platform': 'telegram'
        }

        res = backend.register(payload)
        if not res:
            return False

        self.uuid = res['player_uuid']
        return True
