"""create jobs table

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2024-01-15 10:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),  # hh, linkedin, indeed
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("salary_from", sa.Integer(), nullable=True),
        sa.Column("salary_to", sa.Integer(), nullable=True),
        sa.Column("salary_currency", sa.String(length=10), nullable=True),
        sa.Column("experience", sa.String(length=100), nullable=True),
        sa.Column("employment_type", sa.String(length=100), nullable=True),
        sa.Column(
            "skills",
            postgresql.ARRAY(sa.Text()),
            nullable=True,
            server_default="{}",
        ),
        sa.Column("raw_data", postgresql.JSONB(), nullable=True),
        sa.Column(
            "published_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            onupdate=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Уникальный ключ: один и тот же job с одного источника не дублируется
    op.create_unique_constraint(
        "uq_jobs_source_external_id",
        "jobs",
        ["source", "external_id"],
    )

    # Индексы для частых запросов
    op.create_index("ix_jobs_source", "jobs", ["source"])
    op.create_index("ix_jobs_company", "jobs", ["company"])
    op.create_index("ix_jobs_location", "jobs", ["location"])
    op.create_index("ix_jobs_published_at", "jobs", ["published_at"])
    op.create_index("ix_jobs_salary_from", "jobs", ["salary_from"])

    # GIN индекс для поиска по массиву skills
    op.create_index(
        "ix_jobs_skills_gin",
        "jobs",
        ["skills"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("ix_jobs_skills_gin", table_name="jobs")
    op.drop_index("ix_jobs_salary_from", table_name="jobs")
    op.drop_index("ix_jobs_published_at", table_name="jobs")
    op.drop_index("ix_jobs_location", table_name="jobs")
    op.drop_index("ix_jobs_company", table_name="jobs")
    op.drop_index("ix_jobs_source", table_name="jobs")
    op.drop_constraint("uq_jobs_source_external_id", "jobs", type_="unique")
    op.drop_table("jobs")
