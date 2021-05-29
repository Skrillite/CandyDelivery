"""empty message

Revision ID: 3c33822e9e3e
Revises: 
Create Date: 2021-03-28 21:49:37.841942

"""
from alembic import op
import sqlalchemy as sa

import db


revision = '3c33822e9e3e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('couriers',
    sa.Column('courier_id', sa.Integer(), nullable=False),
    sa.Column('lifting_capacity', sa.Integer(), nullable=False),
    sa.Column('regions', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('working_hours', sa.ARRAY(db.helpers.timerange.TIMERANGE()), nullable=True),
    sa.PrimaryKeyConstraint('courier_id'),
    sa.UniqueConstraint('courier_id')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('courier_id', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Float(precision=2), nullable=False),
    sa.Column('region', sa.Integer(), nullable=False),
    sa.Column('delivery_hours', sa.ARRAY(db.helpers.timerange.TIMERANGE()), nullable=False),
    sa.Column('assign_time', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('complete_time', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('assign_ids', sa.ARRAY(sa.Integer()), nullable=True),
    sa.ForeignKeyConstraint(['courier_id'], ['couriers.courier_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('order_id'),
    sa.UniqueConstraint('order_id')
    )


def downgrade():
    op.drop_table('orders')
    op.drop_table('couriers')
