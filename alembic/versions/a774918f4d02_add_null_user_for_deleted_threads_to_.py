"""Add null user for deleted threads to reference

Revision ID: a774918f4d02
Revises: 12a23a843798
Create Date: 2021-02-11 01:17:53.724536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a774918f4d02'
down_revision = '12a23a843798'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        INSERT INTO sl_users (id, name, tz_offset, archived_at)
            (SELECT 'U0000000000', 'System User', 'UTC-08:00', getdate()
         WHERE NOT EXISTS (SELECT id FROM sl_users WHERE sl_users.id = 'U0000000000'))"""
    )    


def downgrade():
    pass
