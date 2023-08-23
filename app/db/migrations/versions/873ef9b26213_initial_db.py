"""initial-db

Revision ID: 873ef9b26213
Revises: 
Create Date: 2023-08-09 23:21:12.250870

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from app.configs import get_environment

_env = get_environment()

# revision identifiers, used by Alembic.
revision: str = '873ef9b26213'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(f"""         

CREATE TABLE {_env.ENVIRONMENT}.companies (
	id serial4 NOT NULL,
	name varchar(50) NOT NULL,
	CONSTRAINT company_pk PRIMARY KEY (id)
);

CREATE TABLE {_env.ENVIRONMENT}.neighborhoods (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	CONSTRAINT neighborhood_pk PRIMARY KEY (id),
	CONSTRAINT neighborhood_un UNIQUE ("name")
);

CREATE TABLE {_env.ENVIRONMENT}.streets (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	neighborhood_id int4 NOT NULL,
	zip_code varchar NULL,
	CONSTRAINT street_pk PRIMARY KEY (id),
	CONSTRAINT street_fk FOREIGN KEY (neighborhood_id) REFERENCES {_env.ENVIRONMENT}.neighborhoods(id)
);

CREATE TABLE {_env.ENVIRONMENT}.modalities (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	CONSTRAINT modality_pk PRIMARY KEY (id)
);

CREATE TABLE {_env.ENVIRONMENT}.properties (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	code int4 NOT NULL,
	title varchar(255) NULL,
	price double precision NOT NULL,
	description varchar NULL,
	neighborhood_id int4 NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	rooms int2 NOT NULL,
	bathrooms int2 NOT NULL,
	"size" numeric NOT NULL,
	parking_space int2 NOT NULL,
	modality_id int4 NOT NULL,
	image_url varchar NOT NULL,
	property_url varchar NOT NULL,
	"type" varchar NOT NULL,
	street_id int4 NULL,
	"number" varchar(20) NULL,
	is_active bool NOT NULL DEFAULT true,
	CONSTRAINT property_pk PRIMARY KEY (id),
	CONSTRAINT property_unique UNIQUE (company_id, code),
	CONSTRAINT properties_fk FOREIGN KEY (neighborhood_id) REFERENCES {_env.ENVIRONMENT}.neighborhoods(id),
	CONSTRAINT property_fk FOREIGN KEY (company_id) REFERENCES {_env.ENVIRONMENT}.companies(id),
	CONSTRAINT property_modality_fk FOREIGN KEY (modality_id) REFERENCES {_env.ENVIRONMENT}.modalities(id),
	CONSTRAINT property_street_fk FOREIGN KEY (street_id) REFERENCES {_env.ENVIRONMENT}.streets(id)
);

CREATE TABLE {_env.ENVIRONMENT}.property_histories (
	id serial4 NOT NULL,
	property_id int4 NOT NULL,
	price double precision NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT property_histories_pk PRIMARY KEY (id),
	CONSTRAINT property_histories_fk FOREIGN KEY (property_id) REFERENCES {_env.ENVIRONMENT}.properties(id)
);

CREATE TABLE {_env.ENVIRONMENT}.events (
	id uuid NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	sent_to varchar(50) NOT NULL,
	payload jsonb NOT NULL,
	origin varchar(50) NOT NULL,
	CONSTRAINT events_pk PRIMARY KEY (id, origin, sent_to)
);

""")


def downgrade() -> None:
    pass
