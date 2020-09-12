from dataclasses import dataclass
from typing import List, Union
from random import shuffle
from .request_type import UserFeed, UserStatus, UserStatusData
from . import HOST
import requests
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

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
            op = chr(ord('A') + i)
            quest += f'({op}) {self.options[self.ans_map[i]]}\n'

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
        res = None

        if not self.finished:
            res = requests.get(f'{HOST}/v1/players/{self.uid}/feed')
        else:
            res = requests.get(f'{HOST}/v1/players/{self.uid}/rand')

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        feed: UserFeed = res.json()
        data = feed['data']

        if not data:
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
            res = requests.post(f'{HOST}/v1/answers', data=json.dumps(payload))
            logger.info(res.url)
            if not res.ok:
                res.raise_for_status()

        return correct

    def get_status(self) -> UserStatusData:
        res = requests.get(f'{HOST}/v1/players/{self.uid}')
        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        stat: UserStatus = res.json()
        
        return stat['data']

    def register(self) -> bool:
        payload = {
            'name': self.uid,
            'nickname': self.nickname,
            'platform': 'telegram'
        }
        res = requests.post(f'{HOST}/v1/players', data=json.dumps(payload))
        logger.info(res.url)

        return res.ok or res.status_code == 409
