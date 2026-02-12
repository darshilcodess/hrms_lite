"""add attendance table

Revision ID: 002
Revises: 001
Create Date: 2025-02-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

attendance_status_enum = sa.Enum("Present", "Absent", name="attendance_status")


def upgrade() -> None:
    op.create_table(
        "attendance",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("employee_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("status", attendance_status_enum, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.UniqueConstraint("employee_id", "date", name="uq_attendance_employee_date"),
    )


def downgrade() -> None:
    op.drop_table("attendance")
    attendance_status_enum.drop(op.get_bind(), checkfirst=True)
