from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class WorldBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    genre: str | None = Field(default=None, max_length=120)
    subgenre: str | None = Field(default=None, max_length=120)
    tone: str | None = Field(default=None, max_length=180)
    premise: str | None = Field(default=None, max_length=1200)
    description: str | None = Field(default=None, max_length=4000)
    themes_json: list[str] = []
    default_visibility: str = "PRIVATE"
    accent_color: str = "#8B5CF6"
    calendar_mode: str = "YEAR_BASED"


class WorldCreate(WorldBase):
    slug: str | None = Field(default=None, max_length=180)


class WorldUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    genre: str | None = Field(default=None, max_length=120)
    subgenre: str | None = Field(default=None, max_length=120)
    tone: str | None = Field(default=None, max_length=180)
    premise: str | None = Field(default=None, max_length=1200)
    description: str | None = Field(default=None, max_length=4000)
    themes_json: list[str] | None = None
    default_visibility: str | None = None
    accent_color: str | None = None
    calendar_mode: str | None = None


class WorldRead(WorldBase):
    id: int
    owner_id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    archived_at: datetime | None = None

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_entries: int
    characters: int
    factions: int
    locations: int
    events: int
    artifacts: int
    relationships: int
    open_contradictions: int
    draft_entries: int


class RecentEntry(BaseModel):
    id: int
    title: str
    entry_type: str
    status: str
    visibility: str
    importance_level: str
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorldDashboard(BaseModel):
    world: WorldRead
    stats: DashboardStats
    recent_entries: list[RecentEntry]
    major_entries: list[RecentEntry]
    tags: list[str]
