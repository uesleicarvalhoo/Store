"""empty message

Revision ID: c017c35ebee6
Revises: 7ab9eea782b2
Create Date: 2021-08-31 20:30:39.926961

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c017c35ebee6"
down_revision = "7ab9eea782b2"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("items", sa.Column("name", sa.String(), nullable=False))
    op.add_column("items", sa.Column("sugested_sell_value", sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("items", "name")
    op.drop_column("items", "sugested_sell_value")
    # ### end Alembic commands ###