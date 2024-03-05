from db import Repo
import requests
import logging

logger = logging.getLogger(__name__)

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
            return

        t = self.buffer.pop()
        data = dict()
        data["ID"] = self.repo.get_matrix()[1]
        data["text"] = t + " dipped!"
        response = requests.post(self.url, json=data)
        if response.status_code != 200:
            logger.error("post to matrix failed")
        else:
            logger.info("posted to matrix: " + str(data))
