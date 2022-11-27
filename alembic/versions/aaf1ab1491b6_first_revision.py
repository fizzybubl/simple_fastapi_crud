"""first revision

Revision ID: aaf1ab1491b6
Revises: 
Create Date: 2022-11-27 10:07:31.765405

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aaf1ab1491b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("votes", sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"),
                                       nullable=False, primary_key=True),
                    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"),
                              nullable=False, primary_key=True)
                    )
    pass


def downgrade() -> None:
    pass
