from app.db import DBConnection


class Repository:

    def __init__(self, connection: DBConnection) -> None:
        self.conn = connection

    @property
    def conn(self) -> DBConnection:
        return self.conn
