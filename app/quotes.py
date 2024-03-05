import finnhub
from db import Repo
import time
from matrix import Matrix


class Poller:
    NOTIFY_THRESHOLD = 0.95

    def __init__(self, finnhub_api_key: str, repo: Repo, matrix: Matrix):
        self.finnhub_client = finnhub.Client(api_key=finnhub_api_key)
        self.repo = repo
        self.matrix = matrix

    def run(self):
        ticks = self.repo.get_ticks()
        for t in ticks:
            self._runOnce(t, ticks[t])
            time.sleep(1)

    def _runOnce(self, tick, ath):
        quote = self.finnhub_client.quote(tick)
        if "c" in quote:
            if quote["c"] > ath:
                self.repo.upsert_tick(tick, quote["c"])

            if quote["c"] <= Poller.NOTIFY_THRESHOLD * ath:
                self.matrix.notify(tick)
