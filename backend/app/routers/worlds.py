from __future__ import annotations

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database.models import User, World
from app.database.session import get_db
from app.dependencies import get_current_user, get_owned_world
from app.schemas.worlds import WorldCreate, WorldDashboard, WorldRead, WorldUpdate
from app.services.world_service import build_dashboard, create_world, delete_world, list_worlds, update_world

router = APIRouter(prefix="/worlds", tags=["worlds"])


@router.post("", response_model=WorldRead, status_code=201)
def create(payload: WorldCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> World:
    return create_world(db, user, payload)


@router.get("", response_model=list[WorldRead])
def index(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> list[World]:
    return list_worlds(db, user)


@router.get("/{world_id}", response_model=WorldRead)
def show(world: World = Depends(get_owned_world)) -> World:
    return world


@router.patch("/{world_id}", response_model=WorldRead)
def update(payload: WorldUpdate, world: World = Depends(get_owned_world), db: Session = Depends(get_db)) -> World:
    return update_world(db, world, payload)


@router.delete("/{world_id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(world: World = Depends(get_owned_world), db: Session = Depends(get_db)) -> Response:
    delete_world(db, world)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{world_id}/archive", response_model=WorldRead)
def archive(world: World = Depends(get_owned_world), db: Session = Depends(get_db)) -> World:
    from datetime import datetime, timezone

    world.archived_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(world)
    return world


@router.get("/{world_id}/dashboard", response_model=WorldDashboard)
def dashboard(world: World = Depends(get_owned_world), db: Session = Depends(get_db)) -> WorldDashboard:
    return build_dashboard(db, world)
