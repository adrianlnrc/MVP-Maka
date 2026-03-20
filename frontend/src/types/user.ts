export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_verified: boolean;
  subscription_status: "free" | "active" | "cancelled" | "expired";
  subscription_expires_at: string | null;
  created_at: string;
}

export interface UserStats {
  total_days_completed: number;
  streak_days: number;
  longest_streak: number;
  current_day: number | null;
}

export interface ReadingPlanDay {
  id: number;
  day_number: number;
  title: string;
  story_ids: string[];
  bible_passages: string[];
  reflection_prompt: string;
}

export interface ReadingPlan {
  id: number;
  name: string;
  description: string;
  total_days: number;
  is_default: boolean;
}

export interface UserProgress {
  current_day: number;
  streak_days: number;
  longest_streak: number;
  total_days_completed: number;
  plan: ReadingPlan;
}
