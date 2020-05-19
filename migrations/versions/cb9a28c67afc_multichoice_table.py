"""multiChoice table

Revision ID: cb9a28c67afc
Revises: 674466b61ea9
Create Date: 2020-05-19 12:32:27.986513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb9a28c67afc'
down_revision = '674466b61ea9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('multi_choice',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('question', sa.String(length=128), nullable=False),
    sa.Column('choice1', sa.String(length=128), nullable=False),
    sa.Column('choice2', sa.String(length=128), nullable=False),
    sa.Column('choice3', sa.String(length=128), nullable=False),
    sa.Column('choice4', sa.String(length=128), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('multi_choice')
    # ### end Alembic commands ###