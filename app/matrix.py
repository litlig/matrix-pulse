from db import Repo
import requests
import logging

logger = logging.getLogger(__name__)


DEFAULT_MESSAGE = {
    "force": False,
    "icon": 2173,
    "moveIcon": True,
    "repeat": 2,
    "color": [0, 255, 0],
    "data": "Gooood Day"
}

class Matrix:
    def __init__(self, repo: Repo, url: str):
        self.repo = repo
        self.buffer = set()
        self.url = url
        self.boards = repo.get_matrix()

    def notify(self, tick: str) -> None:
        self.buffer.add(tick)

    def run(self) -> None:
        if not self.buffer:
            response = requests.post(self.url, json=DEFAULT_MESSAGE)
            return
        
        t = self.buffer.pop()
        text = t + " dipped!"
        alert = {
            "force": True,
            "icon": 2193,
            "moveIcon": False,
            "repeat": 3,
            "color": [255, 0, 0],
            "data": text
        }
        response = requests.post(self.url, json=alert)
        if response.status_code != 200:
            logger.error("post to matrix failed")
        else:
            logger.info("posted to matrix: " + str(alert))
