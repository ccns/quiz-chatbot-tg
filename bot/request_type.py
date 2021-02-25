from typing import TypedDict, Union

class AnswerReq(TypedDict):
    player_uuid: str
    quiz_uuid: str
    answer: str

class RegisterReq(TypedDict):
    name: str
    platform: str
    platform_userid: str

class UserFeed(TypedDict):
    quiz_uuid: str
    author: str
    domain: str
    description: str
    level: str
    score: int
    options: list[str]

class UserStatus(TypedDict):
    player_uuid: str
    platform_userid: str
    name: str
    platform: str
    correct_count: int
    incorrect_count: int
    no_answer_count: int
    rank: int

class Provoke(TypedDict):
    correct: bool
    message: str

class Answer(TypedDict):
    correct: bool