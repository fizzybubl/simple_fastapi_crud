"""add phone number

Revision ID: ac22923907d8
Revises: aaf1ab1491b6
Create Date: 2022-11-27 10:19:38.810651

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac22923907d8'
down_revision = 'aaf1ab1491b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.add_column('users', sa.Column('phone_number', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    op.create_table('products',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('price', mysql.DECIMAL(precision=15, scale=3), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('promotion', mysql.TINYINT(display_width=1), server_default=sa.text("'0'"), autoincrement=False, nullable=False),
    sa.Column('inventory', mysql.INTEGER(), server_default=sa.text("'0'"), autoincrement=False, nullable=False),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###