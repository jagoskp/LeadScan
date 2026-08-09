"""add_company_and_designation_to_user_profiles

Revision ID: 3e90cecdd8fa
Revises: 
Create Date: 2026-08-09 12:49:52.984332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e90cecdd8fa'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_profiles', sa.Column('company', sa.String(length=255), nullable=True))
    op.add_column('user_profiles', sa.Column('designation', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('user_profiles', 'designation')
    op.drop_column('user_profiles', 'company')
