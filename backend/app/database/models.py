from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    worlds: Mapped[List["World"]] = relationship(back_populates="owner", cascade="all, delete-orphan")


class World(Base, TimestampMixin):
    __tablename__ = "worlds"
    __table_args__ = (UniqueConstraint("owner_id", "slug", name="uq_world_owner_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    slug: Mapped[str] = mapped_column(String(180), index=True, nullable=False)
    genre: Mapped[Optional[str]] = mapped_column(String(120))
    subgenre: Mapped[Optional[str]] = mapped_column(String(120))
    tone: Mapped[Optional[str]] = mapped_column(String(180))
    premise: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    themes_json: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    default_visibility: Mapped[str] = mapped_column(String(40), default="PRIVATE", nullable=False)
    cover_image_path: Mapped[Optional[str]] = mapped_column(String(500))
    accent_color: Mapped[str] = mapped_column(String(20), default="#8B5CF6", nullable=False)
    calendar_mode: Mapped[str] = mapped_column(String(80), default="YEAR_BASED", nullable=False)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    owner: Mapped[User] = relationship(back_populates="worlds")
    entries: Mapped[List["LoreEntry"]] = relationship(back_populates="world", cascade="all, delete-orphan")
    relationships: Mapped[List["LoreRelationship"]] = relationship(back_populates="world", cascade="all, delete-orphan")
    contradictions: Mapped[List["Contradiction"]] = relationship(back_populates="world", cascade="all, delete-orphan")


class LoreEntry(Base, TimestampMixin):
    __tablename__ = "lore_entries"
    __table_args__ = (UniqueConstraint("world_id", "slug", name="uq_entry_world_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    slug: Mapped[str] = mapped_column(String(240), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(60), index=True, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    content_markdown: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(String(40), index=True, nullable=False)
    visibility: Mapped[str] = mapped_column(String(40), nullable=False)
    importance_level: Mapped[str] = mapped_column(String(40), nullable=False)
    color: Mapped[Optional[str]] = mapped_column(String(20))
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    world: Mapped[World] = relationship(back_populates="entries")


class LoreRelationship(Base, TimestampMixin):
    __tablename__ = "relationships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id", ondelete="CASCADE"), index=True, nullable=False)
    source_entry_id: Mapped[int] = mapped_column(ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False)
    target_entry_id: Mapped[int] = mapped_column(ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False)
    relationship_type: Mapped[str] = mapped_column(String(80), nullable=False)
    custom_label: Mapped[Optional[str]] = mapped_column(String(160))
    description: Mapped[Optional[str]] = mapped_column(Text)
    strength: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    directionality: Mapped[str] = mapped_column(String(40), default="DIRECTED", nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="ACTIVE", nullable=False)
    visibility: Mapped[str] = mapped_column(String(40), default="PRIVATE", nullable=False)
    start_year: Mapped[Optional[int]] = mapped_column(Integer)
    end_year: Mapped[Optional[int]] = mapped_column(Integer)

    world: Mapped[World] = relationship(back_populates="relationships")


class Contradiction(Base):
    __tablename__ = "contradictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id", ondelete="CASCADE"), index=True, nullable=False)
    entry_a_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lore_entries.id"))
    entry_b_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lore_entries.id"))
    title: Mapped[str] = mapped_column(String(220), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    resolution_note: Mapped[Optional[str]] = mapped_column(Text)

    world: Mapped[World] = relationship(back_populates="contradictions")


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("world_id", "slug", name="uq_tag_world_slug"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#8B5CF6", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EntryTag(Base):
    __tablename__ = "entry_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey("lore_entries.id", ondelete="CASCADE"), nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    world_id: Mapped[int] = mapped_column(ForeignKey("worlds.id", ondelete="CASCADE"), index=True, nullable=False)
    entry_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lore_entries.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    content_markdown: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[str] = mapped_column(String(40), nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    world_id: Mapped[Optional[int]] = mapped_column(ForeignKey("worlds.id"))
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(120), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer)
    old_values_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    new_values_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
