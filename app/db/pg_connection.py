from psycopg import Connection
from psycopg.rows import dict_row
from .base_connection import DBConnection


class PGConnection(DBConnection):

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def execute(self, sql_statement: str, values: tuple = None, all: bool = False):
        with self.conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(sql_statement, values)
            return cursor.fetchall() if all else cursor.fetchone()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
