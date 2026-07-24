"""initial phase 1 schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-24
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=320), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "worlds",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("slug", sa.String(length=180), nullable=False, index=True),
        sa.Column("genre", sa.String(length=120), nullable=True),
        sa.Column("subgenre", sa.String(length=120), nullable=True),
        sa.Column("tone", sa.String(length=180), nullable=True),
        sa.Column("premise", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("themes_json", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("default_visibility", sa.String(length=40), nullable=False, server_default="PRIVATE"),
        sa.Column("cover_image_path", sa.String(length=500), nullable=True),
        sa.Column("accent_color", sa.String(length=20), nullable=False, server_default="#8B5CF6"),
        sa.Column("calendar_mode", sa.String(length=80), nullable=False, server_default="YEAR_BASED"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("owner_id", "slug", name="uq_world_owner_slug"),
    )
    op.create_table(
        "lore_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("slug", sa.String(length=240), nullable=False),
        sa.Column("entry_type", sa.String(length=60), nullable=False, index=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("content_markdown", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", sa.String(length=40), nullable=False, index=True),
        sa.Column("visibility", sa.String(length=40), nullable=False),
        sa.Column("importance_level", sa.String(length=40), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("world_id", "slug", name="uq_entry_world_slug"),
    )
    op.create_table(
        "relationships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_entry_id", sa.Integer(), sa.ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_entry_id", sa.Integer(), sa.ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relationship_type", sa.String(length=80), nullable=False),
        sa.Column("custom_label", sa.String(length=160), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("strength", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("directionality", sa.String(length=40), nullable=False, server_default="DIRECTED"),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="ACTIVE"),
        sa.Column("visibility", sa.String(length=40), nullable=False, server_default="PRIVATE"),
        sa.Column("start_year", sa.Integer(), nullable=True),
        sa.Column("end_year", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "contradictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entry_a_id", sa.Integer(), sa.ForeignKey("lore_entries.id"), nullable=True),
        sa.Column("entry_b_id", sa.Integer(), sa.ForeignKey("lore_entries.id"), nullable=True),
        sa.Column("title", sa.String(length=220), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("resolution_note", sa.Text(), nullable=True),
    )
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("color", sa.String(length=20), nullable=False, server_default="#8B5CF6"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("world_id", "slug", name="uq_tag_world_slug"),
    )
    op.create_table(
        "entry_tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entry_id", sa.Integer(), sa.ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tag_id", sa.Integer(), sa.ForeignKey("tags.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_table(
        "notes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entry_id", sa.Integer(), sa.ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=True),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("content_markdown", sa.Text(), nullable=False),
        sa.Column("visibility", sa.String(length=40), nullable=False),
        sa.Column("pinned", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("world_id", sa.Integer(), sa.ForeignKey("worlds.id"), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity_type", sa.String(length=120), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("old_values_json", sa.JSON(), nullable=True),
        sa.Column("new_values_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    for table in ["audit_logs", "notes", "entry_tags", "tags", "contradictions", "relationships", "lore_entries", "worlds", "users"]:
        op.drop_table(table)
