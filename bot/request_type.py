from typing import List, TypedDict, Union

class UserFeedData(TypedDict):
    _id: int
    number: str
    tags: List[str]
    description: str
    score: int
    options: List[str]
    hint: Union[str, None]
    answer: str

class UserFeed(TypedDict):
    data: Union[UserFeedData, None]

class UserStatusData(TypedDict):
    _id: int
    name: str
    nickname: str
    platform: str
    rank: int
    score: int
    last: int

class UserStatus(TypedDict):
    data: UserStatusData

class ProvokeData(TypedDict):
    _id: int
    correct: bool
    message: str

class Provoke(TypedDict):
    data: List[ProvokeData]