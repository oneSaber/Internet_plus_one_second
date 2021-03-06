"""first migrate

Revision ID: f83e6efecb82
Revises: 
Create Date: 2018-05-02 16:41:31.368226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f83e6efecb82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('phone_number', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('follows',
    sa.Column('follower_id', sa.Integer(), nullable=False),
    sa.Column('followed_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('picture_name', sa.String(length=64), nullable=True),
    sa.Column('artist_id', sa.String(length=64), nullable=True),
    sa.Column('src', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pictures_picture_name'), 'pictures', ['picture_name'], unique=False)
    op.create_index(op.f('ix_pictures_src'), 'pictures', ['src'], unique=False)
    op.create_table('collections',
    sa.Column('collector_id', sa.Integer(), nullable=False),
    sa.Column('collectedpic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collectedpic_id'], ['pictures.id'], ),
    sa.ForeignKeyConstraint(['collector_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('collector_id', 'collectedpic_id')
    )
    op.create_table('stars',
    sa.Column('staruser_id', sa.Integer(), nullable=False),
    sa.Column('starpic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['starpic_id'], ['pictures.id'], ),
    sa.ForeignKeyConstraint(['staruser_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('staruser_id', 'starpic_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stars')
    op.drop_table('collections')
    op.drop_index(op.f('ix_pictures_src'), table_name='pictures')
    op.drop_index(op.f('ix_pictures_picture_name'), table_name='pictures')
    op.drop_table('pictures')
    op.drop_table('follows')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
