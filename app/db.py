import rocksdb


class Repo:
    TICK_PREFIX = "tick."
    MATRIX_PREFIX = "matrix."

    def __init__(self, db_name):
        self.db = rocksdb.DB(db_name, rocksdb.Options(create_if_missing=True))

    def upsert_tick(self, tick: str, ath: float) -> None:
        k = str.encode(Repo.TICK_PREFIX + tick)
        v = str.encode(str(ath))
        self.db.put(k, v)

    def delete_tick(self, tick: str) -> None:
        k = str.encode(Repo.TICK_PREFIX + tick)
        self.db.delete(k)

    def get_ticks(self) -> dict[str, float]:
        it = self.db.iteritems()
        it.seek(str.encode(Repo.TICK_PREFIX))

        ret = dict()
        for k, v in list(it):
            k = k.decode()
            if not k.startswith(Repo.TICK_PREFIX):
                break
            ret[k.removeprefix(Repo.TICK_PREFIX)] = float(v)

        return ret

    def insert_matrix(self, matrix_id: str) -> None:
        k = str.encode(Repo.MATRIX_PREFIX + matrix_id)
        self.db.put(k, b"")

    def delete_matrix(self, matrix_id: str) -> None:
        k = str.encode(Repo.MATRIX_PREFIX + matrix_id)
        self.db.delete(k)

    def get_matrix(self) -> list[int]:
        it = self.db.iterkeys()
        it.seek(str.encode(Repo.MATRIX_PREFIX))
        ret = []
        for k in list(it):
            k = k.decode()
            if not k.startswith(Repo.MATRIX_PREFIX):
                break
            ret.append(int(k.removeprefix(Repo.MATRIX_PREFIX)))
        return ret
