"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import type { UserProgress, UserStats } from "@/types/user";
import type { ReadingPlanDay } from "@/types/user";

export default function InicioDashboard() {
  const [progress, setProgress] = useState<UserProgress | null>(null);
  const [today, setToday] = useState<ReadingPlanDay | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [progressRes, todayRes, statsRes] = await Promise.all([
          api.get("/api/progress"),
          api.get("/api/reading-plan/today"),
          api.get("/api/users/me/stats"),
        ]);
        setProgress(progressRes.data);
        setToday(todayRes.data);
        setStats(statsRes.data);
      } catch {
        // User might not have started a plan yet
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-8 bg-gray-200 rounded w-64" />
        <div className="grid grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => <div key={i} className="h-32 bg-gray-200 rounded-2xl" />)}
        </div>
        <div className="h-48 bg-gray-200 rounded-2xl" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Bem-vindo de volta</h1>
        <p className="text-gray-500 mt-1">Continue sua jornada bíblica</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Dias concluídos", value: stats?.total_days_completed ?? 0, icon: "✅" },
          { label: "Sequência atual", value: `${stats?.streak_days ?? 0} dias`, icon: "🔥" },
          { label: "Melhor sequência", value: `${stats?.longest_streak ?? 0} dias`, icon: "🏆" },
          { label: "Dia atual", value: stats?.current_day ? `Dia ${stats.current_day}` : "—", icon: "📅" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
            <div className="text-sm text-gray-500">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Today's reading */}
      {today && (
        <div className="bg-brand-900 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-brand-300 text-sm font-medium">Leitura de hoje</p>
              <h2 className="text-xl font-bold mt-1">{today.title}</h2>
            </div>
            <span className="text-3xl">📖</span>
          </div>

          {today.bible_passages.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {today.bible_passages.map((p) => (
                <span key={p} className="bg-brand-800 text-brand-200 text-xs px-3 py-1 rounded-full">
                  {p}
                </span>
              ))}
            </div>
          )}

          {today.reflection_prompt && (
            <p className="text-brand-300 text-sm mb-4 italic">"{today.reflection_prompt}"</p>
          )}

          <Link
            href={`/plano-de-leitura/${today.day_number}`}
            className="inline-flex items-center gap-2 bg-gold-500 hover:bg-gold-400 text-brand-950 font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
          >
            Ler hoje
            <span>→</span>
          </Link>
        </div>
      )}

      {/* Quick links */}
      <div>
        <h2 className="text-lg font-bold text-gray-900 mb-4">Explorar</h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { href: "/cronologia", icon: "📖", label: "Histórias Cronológicas", desc: "12 épocas bíblicas" },
            { href: "/linha-do-tempo", icon: "🗺️", label: "Linha do Tempo", desc: "4.000 anos de história" },
            { href: "/personagens", icon: "👥", label: "Personagens", desc: "De Adão a João" },
          ].map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-brand-200 transition-all"
            >
              <div className="text-2xl mb-2">{item.icon}</div>
              <div className="font-semibold text-gray-900 text-sm">{item.label}</div>
              <div className="text-xs text-gray-400 mt-0.5">{item.desc}</div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
