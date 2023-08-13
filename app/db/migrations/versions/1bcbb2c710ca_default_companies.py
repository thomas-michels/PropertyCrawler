"""default-companies

Revision ID: 1bcbb2c710ca
Revises: 873ef9b26213
Create Date: 2023-08-13 20:37:44.779763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bcbb2c710ca'
down_revision: Union[str, None] = '873ef9b26213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
INSERT INTO public.companies("name") VALUES('Portal Imóveis');
INSERT INTO public.companies("name") VALUES('Zap Imóveis');
               """)


def downgrade() -> None:
    pass
