"""Creating models table

Revision ID: 3cd8f633cb71
Revises: 1bcbb2c710ca
Create Date: 2023-10-23 23:26:21.358344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.configs import get_environment

_env = get_environment()


# revision identifiers, used by Alembic.
revision: str = '3cd8f633cb71'
down_revision: Union[str, None] = '1bcbb2c710ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.execute(f"""
CREATE TABLE {_env.ENVIRONMENT}.models (
	id serial4 NOT NULL,
	"path" varchar NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	x_min_max_scaler varchar NOT NULL,
	neighborhood_encoder varchar NOT NULL,
	one_hot_encoder varchar NOT NULL,
	mse float4 NOT NULL,
	y_min_max_scaler varchar NOT NULL,
	CONSTRAINT models_pk PRIMARY KEY (id)
);
CREATE INDEX models_created_at_idx ON {_env.ENVIRONMENT}.models USING btree (created_at DESC);
               """)


def downgrade() -> None:
    pass
