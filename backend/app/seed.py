from __future__ import annotations

from sqlalchemy import select

from app.core.security import hash_password
from app.database.base import Base
from app.database.models import Contradiction, LoreEntry, LoreRelationship, Tag, User, World
from app.database.session import SessionLocal, engine
from app.utils.slug import slugify


def seed_demo() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
      user = db.scalar(select(User).where(User.email == "demo@loreforge.local"))
      if user is None:
          user = User(email="demo@loreforge.local", display_name="Demo Archivist", password_hash=hash_password("DemoPass123!"))
          db.add(user)
          db.flush()

      world = db.scalar(select(World).where(World.owner_id == user.id, World.slug == "the-ashen-meridian"))
      if world is None:
          world = World(
              owner_id=user.id,
              name="The Ashen Meridian",
              slug="the-ashen-meridian",
              genre="Dark Fantasy",
              tone="Tragic, political, mythic",
              premise="A continent where the sun died once, and every nation claims to be the rightful heir of its light.",
              description="A private demo world for exploring factions, forbidden records, disputed history, and the lightless legacy of empire.",
              themes_json=["Power", "Faith", "Memory", "Inheritance", "Decay"],
              accent_color="#8B5CF6",
          )
          db.add(world)
          db.flush()

          entries = [
              ("Kael Veyr", "CHARACTER", "An exiled imperial knight accused of betraying the emperor.", "CENTRAL"),
              ("Mira Solenne", "CHARACTER", "A prophet who claims to hear the voice of the dead sun.", "CENTRAL"),
              ("Oran Thrice-Bound", "CHARACTER", "An immortal priest-king whose body has been replaced three times.", "MYTHIC"),
              ("Elya Voss", "CHARACTER", "A rebel archivist searching for evidence that official history is false.", "CENTRAL"),
              ("The Ashen Empire", "FACTION", "A grieving empire built around inherited sunlight and military succession.", "MYTHIC"),
              ("The Moonlit Republic", "FACTION", "A mercantile republic that rejects imperial claims to divine light.", "CENTRAL"),
              ("The Choir of Glass", "FACTION", "A secretive order preserving reflections of forbidden suns.", "CENTRAL"),
              ("Veyrhold", "LOCATION", "Capital of the Ashen Empire.", "CENTRAL"),
              ("The Sunken Cathedral", "LOCATION", "A drowned religious site containing forbidden records.", "MYTHIC"),
              ("Port Valen", "LOCATION", "A trading city controlled by the Moonlit Republic.", "MAJOR"),
              ("The Glass Wastes", "LOCATION", "A desert created by an ancient magical plague.", "MYTHIC"),
              ("The Sunfall", "EVENT", "Year 0: the death of the sun and the beginning of disputed inheritance.", "MYTHIC"),
              ("Betrayal at Veyrhold", "EVENT", "Year 103: the event that exiled Kael and fractured imperial legitimacy.", "CENTRAL"),
              ("Mirror of False Suns", "ARTIFACT", "A relic that shows possible histories no court will admit.", "MYTHIC"),
          ]
          by_title = {}
          for title, entry_type, summary, importance in entries:
              entry = LoreEntry(
                  world_id=world.id,
                  title=title,
                  slug=slugify(title),
                  entry_type=entry_type,
                  summary=summary,
                  content_markdown=f"# {title}\n\n{summary}\n\n## Canon notes\n\nSeeded demo lore for Phase 1 dashboards.",
                  status="CANON",
                  visibility="PRIVATE",
                  importance_level=importance,
                  color="#8B5CF6",
                  created_by=user.id,
              )
              db.add(entry)
              db.flush()
              by_title[title] = entry

          links = [
              ("Kael Veyr", "The Ashen Empire", "MEMBER_OF", "Former imperial knight", 5, "FORMER"),
              ("Mira Solenne", "The Sunfall", "WORSHIPS", "Claims the dead sun speaks through dreams", 4, "ACTIVE"),
              ("Elya Voss", "The Sunken Cathedral", "DISCOVERED", "Found evidence of altered records", 5, "SECRET"),
              ("The Ashen Empire", "The Moonlit Republic", "AT_WAR_WITH", "Competing claims to light inheritance", 5, "ACTIVE"),
              ("The Choir of Glass", "Mirror of False Suns", "CREATOR_OF", "Forged the mirror from plague-glass", 4, "DISPUTED"),
              ("Betrayal at Veyrhold", "Kael Veyr", "CAUSED", "Triggered Kael's exile", 5, "ACTIVE"),
              ("Port Valen", "The Moonlit Republic", "LOCATED_IN", "Republic trade capital", 3, "ACTIVE"),
          ]
          for source, target, rel_type, description, strength, status in links:
              db.add(
                  LoreRelationship(
                      world_id=world.id,
                      source_entry_id=by_title[source].id,
                      target_entry_id=by_title[target].id,
                      relationship_type=rel_type,
                      description=description,
                      strength=strength,
                      status=status,
                  )
              )

          for name, color in [
              ("Imperial", "#8B5CF6"),
              ("Forbidden Knowledge", "#DC2626"),
              ("Religious", "#C77900"),
              ("Unreliable History", "#087F8C"),
          ]:
              db.add(Tag(world_id=world.id, name=name, slug=slugify(name), color=color))

          db.add(
              Contradiction(
                  world_id=world.id,
                  entry_a_id=by_title["Kael Veyr"].id,
                  entry_b_id=by_title["Betrayal at Veyrhold"].id,
                  title="Kael appears in accounts after his recorded exile",
                  description="Imperial records say Kael vanished in Year 103, but Moonlit Republic witnesses place him at Port Valen in Year 105.",
                  severity="MEDIUM",
                  status="OPEN",
                  created_by=user.id,
              )
          )

      db.commit()
    finally:
      db.close()


if __name__ == "__main__":
    seed_demo()
    print("Seeded LoreForge demo world.")
