export interface Era {
  id: number;
  slug: string;
  name: string;
  description: string;
  order_index: number;
  approx_date_start: string;
  approx_date_end: string;
  color_hex: string;
  cover_image_url: string | null;
  story_count: number;
}

export interface StoryBrief {
  id: string;
  slug: string;
  title: string;
  summary: string;
  order_index: number;
  reading_time_minutes: number;
  era_id: number;
  themes: string[];
}

export interface CharacterBrief {
  id: string;
  slug: string;
  name: string;
  role: string;
  image_url: string | null;
}

export interface Story {
  id: string;
  slug: string;
  title: string;
  summary: string;
  content: string;
  order_index: number;
  bible_references: string[];
  themes: string[];
  reading_time_minutes: number;
  era: Era;
  characters: CharacterBrief[];
  created_at: string;
  updated_at: string;
}

export interface Character {
  id: string;
  slug: string;
  name: string;
  also_known_as: string[];
  birth_approx: string | null;
  death_approx: string | null;
  biography: string;
  role: string;
  significance: string;
  bible_references: string[];
  image_url: string | null;
  era: Era;
  stories: StoryBrief[];
}

export interface TimelineEvent {
  id: string;
  era_id: number;
  story_id: string | null;
  character_id: string | null;
  title: string;
  description: string;
  event_type: "event" | "birth" | "death" | "miracle" | "war" | "covenant" | "prophecy";
  year_approx: number;
  year_display: string;
  duration_years: number | null;
  order_index: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}
