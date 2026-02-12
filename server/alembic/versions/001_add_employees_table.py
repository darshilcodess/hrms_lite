"""add employees table

Revision ID: 001
Revises:
Create Date: 2025-02-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employee_id", sa.String(length=64), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("department", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_employees_employee_id", "employees", ["employee_id"], unique=True)
    op.create_index("ix_employees_email", "employees", ["email"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_employees_email", table_name="employees")
    op.drop_index("ix_employees_employee_id", table_name="employees")
    op.drop_table("employees")
