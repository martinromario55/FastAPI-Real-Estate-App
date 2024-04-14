"""added a one time password table

Revision ID: 9b7e02cb1cca
Revises: d5046d9533ff
Create Date: 2024-04-14 10:15:12.667761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b7e02cb1cca'
down_revision: Union[str, None] = 'd5046d9533ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_otp',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=6), nullable=False),
    sa.Column('is_valid', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_user_otp_id'), 'user_otp', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_otp_id'), table_name='user_otp')
    op.drop_table('user_otp')
    # ### end Alembic commands ###
