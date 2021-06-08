"""db normalization

Revision ID: 4c9ae42ccb53
Revises: 3c33822e9e3e
Create Date: 2021-05-30 00:46:04.534950

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import db

revision = '4c9ae42ccb53'
down_revision = '3c33822e9e3e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('regions',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('region', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.courier_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('courier_id', 'region')
    )
    op.create_table('working_hours',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('hours', db.helpers.timerange.TIMERANGE(), nullable=False),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.courier_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('courier_id', 'hours')
    )
    op.create_table('assign_ids',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('assign_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['assign_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id', 'assign_id')
    )
    op.create_table('delivery_hours',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('hours', db.helpers.timerange.TIMERANGE(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id', 'hours')
    )
    op.drop_column('couriers', 'regions')
    op.drop_column('couriers', 'working_hours')
    op.drop_column('orders', 'delivery_hours')
    op.drop_column('orders', 'assign_ids')


def downgrade():
    op.add_column('orders', sa.Column('assign_ids', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=True))
    op.add_column('orders', sa.Column('delivery_hours', db.helpers.timerange.TIMERANGE(), autoincrement=False, nullable=False))
    op.add_column('couriers', sa.Column('working_hours', db.helpers.timerange.TIMERANGE(), autoincrement=False, nullable=True))
    op.add_column('couriers', sa.Column('regions', postgresql.ARRAY(sa.INTEGER()), autoincrement=False, nullable=False))
    op.drop_table('delivery_hours')
    op.drop_table('assign_ids')
    op.drop_table('working_hours')
    op.drop_table('regions')
