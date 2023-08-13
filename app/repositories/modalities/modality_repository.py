from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import Modality
from app.configs import get_logger

_logger = get_logger(__name__)


class ModalityRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, name: str) -> Modality:
        try:
            query = '''
            INSERT INTO public.modalities("name")
            VALUES(%(name)s)
            RETURNING id, name;
            '''

            raw_modality = self.conn.execute(sql_statement=query, values={"name": name})
            self.conn.commit()

            if raw_modality:
                return Modality(**raw_modality)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")

    def select_by_id(self, id: int) -> Modality:
        try:
            query = 'SELECT id, "name" FROM public.modalities WHERE id=%(id)s;'

            raw_modality = self.conn.execute(sql_statement=query, values={"id": id})

            if raw_modality:
                return Modality(**raw_modality)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    def select_by_name(self, name: str) -> Modality:
        try:
            query = 'SELECT id, "name" FROM public.modalities WHERE name=%(name)s;'

            raw_modality = self.conn.execute(sql_statement=query, values={"name": name})

            if raw_modality:
                return Modality(**raw_modality)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")
