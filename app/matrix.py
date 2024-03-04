from db import Repo
import requests

"""
curl --header "Content-Type: application/json" \
 -d '{"ID":4, "text": "Google dropped"}' http://192.168.1.117:7000/api/v3/customapp
"""


class Matrix:
    def __init__(self, repo: Repo, url: str):
        self.Repo = repo
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
        data["ID"] = int(4)
        data["text"] = t + " dipped!"
        response = requests.post(self.url, json=data)
        if response.status_code != 200:
            print("post to matrix failed")
