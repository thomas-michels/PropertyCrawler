from app.db import DBConnection
from app.repositories.base_repository import Repository
from app.entities import Company
from app.configs import get_logger
from typing import List

_logger = get_logger(__name__)


class CompanyRepository(Repository):

    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    def select_by_id(self, id: int) -> Company:
        try:
            query = 'SELECT id, "name" FROM public.companies WHERE id=%(id)s;'

            raw_company = self.conn.execute(sql_statement=query, values={"id": id})

            if raw_company:
                return Company(**raw_company)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    def select_by_name(self, name: str) -> Company:
        try:
            query = 'SELECT id, "name" FROM public.companies WHERE name=%(name)s;'

            name = name.lower()

            raw_company = self.conn.execute(sql_statement=query, values={"name": name})

            if raw_company:
                return Company(**raw_company)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")

    def select_all(self) -> List[Company]:
        try:
            query = 'SELECT id, "name" FROM public.companies;'

            raw_companies = self.conn.execute(sql_statement=query, many=True)

            companies = []

            if raw_companies:
                for raw_company in raw_companies:
                    companies.append(Company(**raw_company))

            return companies

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
            return []
