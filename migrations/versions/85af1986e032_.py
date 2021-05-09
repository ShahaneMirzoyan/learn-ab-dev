"""empty message

Revision ID: 85af1986e032
Revises: 
Create Date: 2021-05-09 19:20:03.352598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85af1986e032'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('preview_text', sa.Text(), nullable=False))
    op.add_column('post', sa.Column('sorting_column', sa.Integer(), nullable=True))
    op.add_column('post', sa.Column('custom_html_file', sa.Text(), nullable=True))
    op.add_column('post', sa.Column('slug', sa.String(length=100), nullable=True))
    op.alter_column('post', 'text',
               existing_type=sa.TEXT(),
               nullable=True)
    op.add_column('question', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('question', sa.Column('sorting_column', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'sorting_column')
    op.drop_column('question', 'created_at')
    op.alter_column('post', 'text',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('post', 'slug')
    op.drop_column('post', 'custom_html_file')
    op.drop_column('post', 'sorting_column')
    op.drop_column('post', 'preview_text')
    # ### end Alembic commands ###
