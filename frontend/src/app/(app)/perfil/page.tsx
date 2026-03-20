"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import type { UserStats } from "@/types/user";

export default function PerfilPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    api.get("/api/users/me/stats").then((r) => setStats(r.data)).catch(() => {});
  }, []);

  return (
    <div className="max-w-lg space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Meu Perfil</h1>

      {/* User info */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-14 h-14 bg-brand-600 rounded-full flex items-center justify-center text-white text-xl font-bold">
            {user?.full_name?.charAt(0).toUpperCase() || "?"}
          </div>
          <div>
            <p className="font-bold text-gray-900 text-lg">{user?.full_name}</p>
            <p className="text-gray-500 text-sm">{user?.email}</p>
            <span
              className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium mt-1 ${
                user?.subscription_status === "active"
                  ? "bg-green-100 text-green-700"
                  : "bg-gray-100 text-gray-500"
              }`}
            >
              {user?.subscription_status === "active" ? "Completo" : "Gratuito"}
            </span>
          </div>
        </div>

        {stats && (
          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.total_days_completed}</p>
              <p className="text-sm text-gray-500">Dias de leitura</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.streak_days}</p>
              <p className="text-sm text-gray-500">Dias em sequência</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{stats.longest_streak}</p>
              <p className="text-sm text-gray-500">Melhor sequência</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {stats.current_day ? `Dia ${stats.current_day}` : "—"}
              </p>
              <p className="text-sm text-gray-500">Dia atual</p>
            </div>
          </div>
        )}
      </div>

      {user?.subscription_status !== "active" && (
        <div className="bg-brand-50 border border-brand-200 rounded-2xl p-5">
          <p className="font-semibold text-brand-900 mb-1">Desbloqueie o acesso completo</p>
          <p className="text-sm text-brand-700 mb-4">
            200+ histórias, linha do tempo completa, plano 365 dias e muito mais por apenas R$47,90.
          </p>
          <a
            href="/#pricing"
            className="inline-flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white font-semibold px-5 py-2.5 rounded-xl text-sm transition-colors"
          >
            Ver planos
          </a>
        </div>
      )}
    </div>
  );
}
