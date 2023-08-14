from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import PropertyHistoryInDB, PropertyHistory
from app.configs import get_logger
from typing import List

_logger = get_logger(__name__)


class PropertyHistoryRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, property_history: PropertyHistory) -> PropertyHistoryInDB:
        try:
            query = '''
            INSERT INTO public.property_histories
            (property_id, price, created_at, updated_at)
            VALUES(%(property_id)s, %(price)s, NOW(), NOW())
            RETUNING id, property_id, price, created_at, updated_at;
            '''
            raw_history = self.conn.execute(sql_statement=query, values=property_history.model_dump())

            if raw_history:
                return PropertyHistoryInDB(**raw_history)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {property_history.model_dump('json')}")

    def select_by_property_id(self, property_id: int) -> List[PropertyHistoryInDB]:
        try:
            query = '''
            SELECT id, property_id, price, created_at, updated_at
            FROM public.property_histories
            WHERE property_id=%(property_id)s;
            '''

            raw_histories = self.conn.execute(sql_statement=query, values={"property_id": property_id}, many=True)

            histories = []

            if raw_histories:
                for raw_history in raw_histories:
                    histories.append(PropertyHistoryInDB(**raw_history))

            return histories

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(property_id=property_id)}")
            return []
