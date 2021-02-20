import logging
import requests
from urllib.parse import urljoin
from typing import Any, Dict, Union
from http import HTTPStatus
from .request_type import AnswerReq, RegisterReq, UserFeed, UserStatus, Provoke, Answer
from .config import HOST

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_status(uuid: str) -> UserStatus:
    res = requests.get(urljoin(HOST, f'/players/{uuid}/'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def get_feed(uuid: str) -> Union[UserFeed, None]:
    res = requests.get(urljoin(HOST, f'/feeds/{uuid}'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    if res.status_code == HTTPStatus.NO_CONTENT:
        return None
    else:
        return res.json()

def get_rand_feed() -> UserFeed:
    res = requests.get(urljoin(HOST, f'/rand/'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def get_provokes() -> list[Provoke]:
    res = requests.get(urljoin(HOST, '/provokes/'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def post_answer(payload: AnswerReq) -> Answer:
    res = requests.post(urljoin(HOST, '/answers/'), json=payload)

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def register(payload: RegisterReq) -> Union[UserStatus, None]:
    res = requests.post(urljoin(HOST, '/players/'), json=payload)
    logger.info(res.url)

    if not (res.ok or res.status_code == HTTPStatus.CONFLICT):
        return

    return res.json()

def search(userid: str) -> Union[UserStatus, None]:
    res = requests.get(urljoin(HOST, f'/mappings/{userid}/'))
    logger.info(res.url)

    if not res.ok:
        return

    return res.json()