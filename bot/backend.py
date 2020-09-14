import logging
from urllib.parse import urljoin
from typing import Any, Dict

import requests
from .request_type import UserFeed, UserStatus, Provoke
from .config import HOST

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def get_status(uid: str) -> UserStatus:
    res = requests.get(urljoin(HOST, f'v1/players/{uid}'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def get_feed(uid: str) -> UserFeed:
    res = requests.get(urljoin(HOST, f'v1/players/{uid}/feed'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def get_rand_feed(uid: str) -> UserFeed:
    res = requests.get(urljoin(HOST, f'v1/players/{uid}/rand'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def get_provokes() -> Provoke:
    res = requests.get(urljoin(HOST, 'v1/provokes'))

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

    return res.json()

def post_answer(payload: Dict[str, Any]) -> None:
    res = requests.post(urljoin(HOST, 'v1/answers'), json=payload)

    logger.info(res.url)
    if not res.ok:
        res.raise_for_status()

def register(payload) -> bool:
    res = requests.post(urljoin(HOST, '/v1/players'), json=payload)
    logger.info(res.url)

    if res.ok or res.status_code == 409:
        return True
    else:
        res.raise_for_status()
        return False
