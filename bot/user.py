from dataclasses import dataclass
from typing import List, Union
from random import shuffle

from .backend import backend

@dataclass
class Problem:
    _id: int
    category: str
    question: str
    options: List[str]
    answer: str
    hint: Union[str, None] = None
    ans_map: Union[List[int], None] = None

    def __post_init__(self):
        if not self.ans_map:
            self.ans_map = list(range(len(self.options)))
            shuffle(self.ans_map)

    def text(self):
        quest = f'<b>[{self.category}]</b>\n{self.question}\n'

        for i in range(len(self.options)):
            opchar = chr(ord('A') + i)
            quest += f'({opchar}) {self.options[self.ans_map[i]]}\n'

        return quest

@dataclass
class User:
    uid: str
    nickname: str
    prob: Union[Problem, None] = None
    finished: bool = False

    def __post_init__(self):
        self.uid = 'telegram-' + self.uid

    def get_problem(self) -> Union[Problem, None]:
        if not self.finished:
            feed = backend.get_feed(self.uid)
        else:
            feed = backend.get_rand_feed(self.uid)

        data = feed['data']
        if not data:
            self.finished = True
            return None

        self.prob = Problem(
            data['_id'],
            data['tags'][0],
            data['description'],
            data['options'],
            data['answer'],
            data['hint']
        )
        return self.prob

    def check_answer(self, ans: str) -> bool:
        ans = chr(self.prob.ans_map[int(ans)] + ord('A'))
        correct = self.prob.answer == ans

        if not self.finished:
            payload = {
                'player_name': self.uid,
                'quiz_number': self.prob._id,
                'correct': correct
            }
            backend.post_answer(payload)

        return correct

    def get_status(self):
        stat = backend.get_status(self.uid)
        return stat['data']

    def register(self) -> bool:
        payload = {
            'name': self.uid,
            'nickname': self.nickname,
            'platform': 'telegram'
        }
        success = backend.register(payload)
        return success
