# Database Notes

## Phase 1 tables

- `users`
- `worlds`
- `lore_entries`
- `relationships`
- `tags`
- `entry_tags`
- `notes`
- `contradictions`
- `audit_logs`

## Ownership

Worlds belong to users through `worlds.owner_id`. API dependencies verify ownership before returning world detail or dashboard data.

## Future profiles

Character, faction, location, event, and artifact profile tables should reference `lore_entries.id` so every specialized object remains searchable and relationship-ready through the shared entry model.
