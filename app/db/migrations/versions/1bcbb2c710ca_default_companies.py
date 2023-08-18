"""default-companies

Revision ID: 1bcbb2c710ca
Revises: 873ef9b26213
Create Date: 2023-08-13 20:37:44.779763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.configs import get_environment

_env = get_environment()


# revision identifiers, used by Alembic.
revision: str = '1bcbb2c710ca'
down_revision: Union[str, None] = '873ef9b26213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = '873ef9b26213'


def upgrade() -> None:
    op.execute(f"""
INSERT INTO {_env.ENVIRONMENT}.companies("name") VALUES('Portal Imóveis');
INSERT INTO {_env.ENVIRONMENT}.companies("name") VALUES('Zap Imóveis');
               """)


def downgrade() -> None:
    pass
