"""Added required tables

Revision ID: c79e9ee680da
Revises: 
Create Date: 2024-05-06 13:35:41.963073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c79e9ee680da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genders',
    sa.Column('gender_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('gender_name', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.PrimaryKeyConstraint('gender_id')
    )
    op.create_table('intentions',
    sa.Column('intention_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('intention_name', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('intention_icon_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('intention_id')
    )
    op.create_table('interests',
    sa.Column('interest_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('interest_name', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('interest_icon_url', sa.String(), nullable=True),
    sa.Column('category', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('interest_id')
    )
    op.create_table('locations',
    sa.Column('location_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('medias',
    sa.Column('media_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('media_url', sa.String(), nullable=False),
    sa.Column('is_approved', sa.Boolean(), nullable=True),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('media_id')
    )
    op.create_table('preferences',
    sa.Column('preference_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('genders_ids', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('distance_range', sa.Integer(), nullable=True),
    sa.Column('use_distance', sa.Boolean(), nullable=True),
    sa.Column('age_min', sa.Integer(), nullable=True),
    sa.Column('age_max', sa.Integer(), nullable=True),
    sa.Column('use_age', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('preference_id')
    )
    op.create_table('statuses',
    sa.Column('status_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('suspend_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('status_id')
    )
    op.create_table('profile_medias',
    sa.Column('profile_media_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('media_1_id', sa.Integer(), nullable=True),
    sa.Column('media_2_id', sa.Integer(), nullable=True),
    sa.Column('media_3_id', sa.Integer(), nullable=True),
    sa.Column('media_4_id', sa.Integer(), nullable=True),
    sa.Column('media_5_id', sa.Integer(), nullable=True),
    sa.Column('media_6_id', sa.Integer(), nullable=True),
    sa.Column('media_7_id', sa.Integer(), nullable=True),
    sa.Column('media_8_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['media_1_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_2_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_3_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_4_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_5_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_6_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_7_id'], ['medias.media_id'], ),
    sa.ForeignKeyConstraint(['media_8_id'], ['medias.media_id'], ),
    sa.PrimaryKeyConstraint('profile_media_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('fullname', sa.String(), nullable=False),
    sa.Column('birthday', sa.DateTime(), nullable=False),
    sa.Column('show_me', sa.Boolean(), nullable=False),
    sa.Column('height', sa.Integer(), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('registration_date', sa.DateTime(), nullable=True),
    sa.Column('gender_id', sa.Integer(), nullable=True),
    sa.Column('preference_id', sa.Integer(), nullable=True),
    sa.Column('intention_id', sa.Integer(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('profile_media_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=True),
    sa.Column('interests_ids', sa.ARRAY(sa.Integer()), nullable=True),
    sa.ForeignKeyConstraint(['gender_id'], ['genders.gender_id'], ),
    sa.ForeignKeyConstraint(['intention_id'], ['intentions.intention_id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.ForeignKeyConstraint(['preference_id'], ['preferences.preference_id'], ),
    sa.ForeignKeyConstraint(['profile_media_id'], ['profile_medias.profile_media_id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.status_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('dating',
    sa.Column('dating_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_from_uuid', sa.UUID(), nullable=True),
    sa.Column('user_to_uuid', sa.UUID(), nullable=True),
    sa.Column('dating_type', sa.String(), nullable=True),
    sa.Column('dating_text', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_from_uuid'], ['users.user_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_to_uuid'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('dating_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dating')
    op.drop_table('users')
    op.drop_table('profile_medias')
    op.drop_table('statuses')
    op.drop_table('preferences')
    op.drop_table('medias')
    op.drop_table('locations')
    op.drop_table('interests')
    op.drop_table('intentions')
    op.drop_table('genders')
    # ### end Alembic commands ###
