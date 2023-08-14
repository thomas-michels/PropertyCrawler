from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import Neighborhood
from app.configs import get_logger

_logger = get_logger(__name__)


class NeighborhoodRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, name: str) -> Neighborhood:
        try:
            query = '''
            INSERT INTO public.neighborhoods("name")
            VALUES(%(name)s)
            RETURNING id, name;
            '''

            raw_neighborhood = self.conn.execute(sql_statement=query, values={"name": name})

            if raw_neighborhood:
                return Neighborhood(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")

    def select_by_id(self, id: int) -> Neighborhood:
        try:
            query = 'SELECT id, "name" FROM public.neighborhoods WHERE id=%(id)s;'

            raw_neighborhood = self.conn.execute(sql_statement=query, values={"id": id})

            if raw_neighborhood:
                return Neighborhood(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    def select_by_name(self, name: str) -> Neighborhood:
        try:
            query = 'SELECT id, "name" FROM public.neighborhoods WHERE name=%(name)s;'

            raw_neighborhood = self.conn.execute(sql_statement=query, values={"name": name})

            if raw_neighborhood:
                return Neighborhood(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")
