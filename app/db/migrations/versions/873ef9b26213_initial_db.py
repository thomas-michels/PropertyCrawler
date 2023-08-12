"""initial-db

Revision ID: 873ef9b26213
Revises: 
Create Date: 2023-08-09 23:21:12.250870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '873ef9b26213'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE public.companies (
	id serial4 NOT NULL,
	name varchar(50) NOT NULL,
	CONSTRAINT company_pk PRIMARY KEY (id)
);

CREATE TABLE public.neighborhoods (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	CONSTRAINT neighborhood_pk PRIMARY KEY (id),
	CONSTRAINT neighborhood_un UNIQUE ("name")
);

CREATE TABLE public.modalities (
	id serial4 NOT NULL,
	"name" varchar(50) NOT NULL,
	CONSTRAINT modality_pk PRIMARY KEY (id)
);

CREATE TABLE public.streets (
	id int4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT street_pk PRIMARY KEY (id)
);

CREATE TABLE public.properties (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	code int4 NOT NULL,
	title varchar(255) NULL,
	price money NOT NULL,
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
	CONSTRAINT property_pk PRIMARY KEY (id),
	CONSTRAINT property_unique UNIQUE (company_id, code),
	CONSTRAINT properties_fk FOREIGN KEY (neighborhood_id) REFERENCES public.neighborhoods(id),
	CONSTRAINT property_fk FOREIGN KEY (company_id) REFERENCES public.companies(id),
	CONSTRAINT property_modality_fk FOREIGN KEY (modality_id) REFERENCES public.modalities(id),
	CONSTRAINT property_street_fk FOREIGN KEY (street_id) REFERENCES public.streets(id)
);

""")


def downgrade() -> None:
    pass
