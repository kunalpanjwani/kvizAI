"""Add quiz templates table

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create quiz_templates table
    op.create_table('quiz_templates',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('subject', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('questions', sa.JSON(), nullable=False),
        sa.Column('correct_answers', sa.JSON(), nullable=False),
        sa.Column('difficulty', sa.String(length=20), nullable=False),
        sa.Column('time_limit', sa.Integer(), nullable=True),
        sa.Column('question_count', sa.Integer(), nullable=False),
        sa.Column('max_score', sa.Integer(), nullable=False),
        sa.Column('template_type', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=True),
        sa.Column('times_used', sa.Integer(), nullable=True),
        sa.Column('average_score', sa.Integer(), nullable=True),
        sa.Column('average_time', sa.Integer(), nullable=True),
        sa.Column('schedule_type', sa.String(length=20), nullable=True),
        sa.Column('next_schedule', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_scheduled', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('language', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for better performance
    op.create_index(op.f('ix_quiz_templates_subject'), 'quiz_templates', ['subject'], unique=False)
    op.create_index(op.f('ix_quiz_templates_category'), 'quiz_templates', ['category'], unique=False)
    op.create_index(op.f('ix_quiz_templates_template_type'), 'quiz_templates', ['template_type'], unique=False)
    op.create_index(op.f('ix_quiz_templates_is_active'), 'quiz_templates', ['is_active'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index(op.f('ix_quiz_templates_is_active'), table_name='quiz_templates')
    op.drop_index(op.f('ix_quiz_templates_template_type'), table_name='quiz_templates')
    op.drop_index(op.f('ix_quiz_templates_category'), table_name='quiz_templates')
    op.drop_index(op.f('ix_quiz_templates_subject'), table_name='quiz_templates')
    
    # Drop quiz_templates table
    op.drop_table('quiz_templates') 