from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.models import Contradiction, LoreEntry, LoreRelationship, Tag, User, World
from app.schemas.worlds import DashboardStats, RecentEntry, WorldCreate, WorldDashboard, WorldUpdate
from app.utils.slug import slugify


def _unique_world_slug(db: Session, owner_id: int, base_slug: str) -> str:
    slug = slugify(base_slug)
    candidate = slug
    counter = 2
    while db.scalar(select(World).where(World.owner_id == owner_id, World.slug == candidate)) is not None:
        candidate = f"{slug}-{counter}"
        counter += 1
    return candidate


def create_world(db: Session, owner: User, payload: WorldCreate) -> World:
    world = World(
        owner_id=owner.id,
        name=payload.name.strip(),
        slug=_unique_world_slug(db, owner.id, payload.slug or payload.name),
        genre=payload.genre,
        subgenre=payload.subgenre,
        tone=payload.tone,
        premise=payload.premise,
        description=payload.description,
        themes_json=payload.themes_json,
        default_visibility=payload.default_visibility,
        accent_color=payload.accent_color,
        calendar_mode=payload.calendar_mode,
    )
    db.add(world)
    db.commit()
    db.refresh(world)
    return world


def list_worlds(db: Session, owner: User) -> list[World]:
    return list(db.scalars(select(World).where(World.owner_id == owner.id, World.archived_at.is_(None)).order_by(World.updated_at.desc())))


def update_world(db: Session, world: World, payload: WorldUpdate) -> World:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(world, key, value)
    db.commit()
    db.refresh(world)
    return world


def delete_world(db: Session, world: World) -> None:
    db.delete(world)
    db.commit()


def build_dashboard(db: Session, world: World) -> WorldDashboard:
    type_counts = dict(
        db.execute(
            select(LoreEntry.entry_type, func.count(LoreEntry.id)).where(LoreEntry.world_id == world.id).group_by(LoreEntry.entry_type)
        ).all()
    )
    total_entries = db.scalar(select(func.count(LoreEntry.id)).where(LoreEntry.world_id == world.id)) or 0
    relationships = db.scalar(select(func.count(LoreRelationship.id)).where(LoreRelationship.world_id == world.id)) or 0
    open_contradictions = db.scalar(
        select(func.count(Contradiction.id)).where(Contradiction.world_id == world.id, Contradiction.status.in_(["OPEN", "REVIEWING"]))
    ) or 0
    draft_entries = db.scalar(select(func.count(LoreEntry.id)).where(LoreEntry.world_id == world.id, LoreEntry.status == "DRAFT")) or 0
    recent_entries = list(
        db.scalars(select(LoreEntry).where(LoreEntry.world_id == world.id).order_by(LoreEntry.updated_at.desc()).limit(6))
    )
    major_entries = list(
        db.scalars(
            select(LoreEntry)
            .where(LoreEntry.world_id == world.id, LoreEntry.importance_level.in_(["CENTRAL", "MYTHIC"]))
            .order_by(LoreEntry.updated_at.desc())
            .limit(6)
        )
    )
    tags = list(db.scalars(select(Tag.name).where(Tag.world_id == world.id).order_by(Tag.name.asc()).limit(12)))
    return WorldDashboard(
        world=world,
        stats=DashboardStats(
            total_entries=total_entries,
            characters=type_counts.get("CHARACTER", 0),
            factions=type_counts.get("FACTION", 0),
            locations=type_counts.get("LOCATION", 0),
            events=type_counts.get("EVENT", 0),
            artifacts=type_counts.get("ARTIFACT", 0),
            relationships=relationships,
            open_contradictions=open_contradictions,
            draft_entries=draft_entries,
        ),
        recent_entries=[RecentEntry.model_validate(entry) for entry in recent_entries],
        major_entries=[RecentEntry.model_validate(entry) for entry in major_entries],
        tags=tags,
    )


def ensure_world_is_owned(world: World | None, owner: User) -> World:
    if world is None or world.owner_id != owner.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="World not found")
    return world
