"""specify completed col: not null and defualt false

Revision ID: 2dd8f190bfa0
Revises: 45036c080169
Create Date: 2024-12-10 21:09:32.502516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2dd8f190bfa0'
down_revision = '45036c080169'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Assign a default value (False) to all rows in the `completed` column
    op.execute('UPDATE todos SET completed = FALSE WHERE completed IS NULL')
    
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('completed',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('todos', schema=None) as batch_op:
        batch_op.alter_column('completed',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###
