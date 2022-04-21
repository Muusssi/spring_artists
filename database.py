
import psycopg2


class Database():

    def __init__(self, pw):
        self.pw = pw
        self._conn = None

    def _connect(self):
        self._conn = psycopg2.connect(f"dbname='art' host='localhost' password='{self.pw}'")

    def _cursor(self):
        return self._conn.cursor()

    def _close_connection(self):
        self._conn.close()

    def _commit(self):
        self._conn.commit()

    def reconnect(self):
        self._close_connection()
        self._connect()
