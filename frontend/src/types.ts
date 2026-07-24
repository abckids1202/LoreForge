export interface User {
  id: number;
  email: string;
  display_name: string;
  active: boolean;
}

export interface World {
  id: number;
  owner_id: number;
  name: string;
  slug: string;
  genre: string | null;
  subgenre: string | null;
  tone: string | null;
  premise: string | null;
  description: string | null;
  themes_json: string[];
  default_visibility: string;
  accent_color: string;
  calendar_mode: string;
  created_at: string;
  updated_at: string;
  archived_at: string | null;
}

export interface DashboardStats {
  total_entries: number;
  characters: number;
  factions: number;
  locations: number;
  events: number;
  artifacts: number;
  relationships: number;
  open_contradictions: number;
  draft_entries: number;
}

export interface RecentEntry {
  id: number;
  title: string;
  entry_type: string;
  status: string;
  visibility: string;
  importance_level: string;
  updated_at: string;
}

export interface WorldDashboard {
  world: World;
  stats: DashboardStats;
  recent_entries: RecentEntry[];
  major_entries: RecentEntry[];
  tags: string[];
}
