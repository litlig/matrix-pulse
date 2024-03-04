import finnhub
from db import Repo
import time


class Poller:
    NOTIFY_THRESHOLD = 0.95

    def __init__(self, finnhub_api_key: str, repo: Repo):
        self.finnhub_client = finnhub.Client(api_key=finnhub_api_key)
        self.repo = repo
        self.update()

    def update(self):
        self.ticks = self.repo.get_ticks()

    def run(self):
        for t in self.ticks:
            self._runOnce(t)
            time.sleep(1)

    def _runOnce(self, tick):
        quote = self.finnhub_client.quote(tick)
        if "c" in quote:
            if quote["c"] > self.ticks[tick]:
                self.ticks[tick] = quote["c"]
                self.repo.upsert_tick(tick, quote["c"])

            if quote["c"] <= 0.95 * self.ticks[tick]:
                self.notify(tick)
