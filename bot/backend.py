import configparser
import logging
from urllib.parse import urljoin
from typing import Any, Dict

import requests
from .request_type import UserFeed, UserStatus, Provoke

config = configparser.ConfigParser()
config.read('.config')
HOST = config['Bot']['Host']

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Backend:
    def get_status(self, uid: str) -> UserStatus:
        res = requests.get(urljoin(HOST, f'v1/players/{uid}'))

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        return res.json()

    def get_feed(self, uid: str) -> UserFeed:
        res = requests.get(urljoin(HOST, f'v1/players/{uid}/feed'))

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        return res.json()

    def get_rand_feed(self, uid: str) -> UserFeed:
        res = requests.get(urljoin(HOST, f'v1/players/{uid}/rand'))

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        return res.json()

    def get_provokes(self) -> Provoke:
        res = requests.get(urljoin(HOST, 'v1/provokes'))

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

        return res.json()

    def post_answer(self, payload: Dict[str, Any]) -> None:
        res = requests.post(urljoin(HOST, 'v1/answers'), json=payload)

        logger.info(res.url)
        if not res.ok:
            res.raise_for_status()

    def register(self, payload) -> bool:
        res = requests.post(urljoin(HOST, '/v1/players'), json=payload)
        logger.info(res.url)

        if res.ok or res.status_code == 409:
            return True
        else:
            res.raise_for_status()
            return False

backend = Backend()
