from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import Property, PropertyInDB, SimpleProperty
from app.configs import get_logger
from typing import List
from psycopg.errors import UniqueViolation

_logger = get_logger(__name__)


class PropertyRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def insert(self, property: Property) -> PropertyInDB:
        try:
            query = '''
            INSERT INTO public.properties
            (company_id, code, title, price, description, neighborhood_id,
            created_at, updated_at, rooms, bathrooms, "size", parking_space,
            modality_id, image_url, property_url, "type", street_id, "number", is_active)
            VALUES(%(company_id)s, %(code)s, %(title)s, %(price)s, %(description)s, %(neighborhood_id)s,
            %(created_at)s, %(updated_at)s, %(rooms)s, %(bathrooms)s, %(size)s, %(parking_space)s,
            %(modality_id)s, %(image_url)s, %(property_url)s, %(type)s, %(street_id)s, %(number)s, true)
            RETURNING id, company_id, code, title, price, description, neighborhood_id,
            created_at, updated_at, rooms, bathrooms, "size", parking_space,
            modality_id, image_url, property_url, "type", street_id, "number", is_active;
            '''
            raw_property = self.conn.execute(
                sql_statement=query,
                values=property.model_dump())

            if raw_property:
                return PropertyInDB(**raw_property)
            
        except UniqueViolation:
            return False

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {property.model_dump(mode='json')}")

    def select_by_id(self, id: int) -> PropertyInDB:
        try:
            query = '''
            SELECT id, company_id, code, title, price, description, neighborhood_id,
            created_at, updated_at, rooms, bathrooms, "size", parking_space,
            modality_id, image_url, property_url, "type", street_id, "number", is_active
            FROM public.properties
            WHERE id=%(id)s;
            '''
            raw_property = self.conn.execute(sql_statement=query, values={"id": id})

            if raw_property:
                return PropertyInDB(**raw_property)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    def select_by_code_and_company(self, code: int, company_id: int) -> PropertyInDB:
        try:
            query = '''
            SELECT id, company_id, code, title, price, description, neighborhood_id,
            created_at, updated_at, rooms, bathrooms, "size", parking_space,
            modality_id, image_url, property_url, "type", street_id, "number", is_active
            FROM public.properties
            WHERE code=%(code)s AND company_id=%(company_id)s;
            '''
            raw_property = self.conn.execute(sql_statement=query, values={"code": code, "company_id": company_id})

            if raw_property:
                return PropertyInDB(**raw_property)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(code=code, company_id=company_id)}")

    def select_all_codes(self, active: bool = False) -> List[SimpleProperty]:
        try:
            query = 'SELECT id, company_id, code, property_url FROM public.neighborhoods WHERE is_active=%(is_active)s;'

            raw_properties = self.conn.execute(sql_statement=query, values={"is_active": active}, many=True)

            properties = []

            if raw_properties:
                for raw_property in raw_properties:
                    properties.append(SimpleProperty(**raw_property))

            return properties

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
            return []
        
    def select_by_url(self, url: str) -> PropertyInDB:
        query = '''
        SELECT id, company_id, code, title, price, description, neighborhood_id,
        created_at, updated_at, rooms, bathrooms, "size", parking_space,
        modality_id, image_url, property_url, "type", street_id, "number", is_active
        FROM public.properties
        WHERE property_url=%(property_url)s;
        '''
        raw_property = self.conn.execute(sql_statement=query, values={"property_url": url})

        if raw_property:
            return PropertyInDB(**raw_property)

    def update_price(self, id: int, new_price: float) -> bool:
        try:
            query = '''
            UPDATE
                public.properties
            SET
                price = %(price)s,
                updated_at = NOW()
            WHERE id=%(id)s
            RETURNING 1;
            '''
            raw = self.conn.execute(sql_statement=query, values={"id": id, "price": new_price})
            return bool(raw)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")
            return False

    def delete(self, id: int) -> bool:
        try:
            query = '''
            UPDATE
                public.properties
            SET
                is_active = false,
                updated_at = NOW()
            WHERE id=%(id)s
            RETURNING 1;
            '''
            raw = self.conn.execute(sql_statement=query, values={"id": id})
            return bool(raw)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")
            return False
