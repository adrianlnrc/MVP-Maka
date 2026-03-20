"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import type { UserProgress } from "@/types/user";

export default function PlanoPage() {
  const [progress, setProgress] = useState<UserProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    api.get("/api/progress")
      .then((r) => setProgress(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  async function startPlan() {
    setStarting(true);
    try {
      const r = await api.post("/api/reading-plan/start");
      setProgress(r.data);
    } finally {
      setStarting(false);
    }
  }

  if (loading) {
    return <div className="animate-pulse h-64 bg-gray-200 rounded-2xl" />;
  }

  const completedPercent = progress
    ? Math.round((progress.total_days_completed / progress.plan.total_days) * 100)
    : 0;

  return (
    <div className="max-w-2xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Plano de Leitura</h1>
        <p className="text-gray-500 mt-1">
          {progress?.plan.name || "Bíblia Cronológica em 365 dias"}
        </p>
      </div>

      {progress ? (
        <>
          {/* Progress overview */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-sm text-gray-500">Progresso geral</p>
                <p className="text-3xl font-bold text-gray-900">{completedPercent}%</p>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Dias concluídos</p>
                <p className="text-xl font-bold text-brand-700">
                  {progress.total_days_completed} / {progress.plan.total_days}
                </p>
              </div>
            </div>

            <div className="w-full bg-gray-100 rounded-full h-3 mb-4">
              <div
                className="bg-brand-600 h-3 rounded-full transition-all"
                style={{ width: `${completedPercent}%` }}
              />
            </div>

            <div className="flex gap-6 text-sm">
              <div className="flex items-center gap-2">
                <span className="text-orange-500">🔥</span>
                <span className="text-gray-600">
                  <span className="font-bold text-gray-900">{progress.streak_days}</span> dias seguidos
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span>🏆</span>
                <span className="text-gray-600">
                  Recorde: <span className="font-bold text-gray-900">{progress.longest_streak}</span> dias
                </span>
              </div>
            </div>
          </div>

          {/* Today CTA */}
          <div className="bg-brand-900 rounded-2xl p-6 text-white">
            <p className="text-brand-300 text-sm mb-1">Dia atual</p>
            <p className="text-3xl font-bold mb-4">Dia {progress.current_day}</p>
            <Link
              href={`/plano-de-leitura/${progress.current_day}`}
              className="inline-flex items-center gap-2 bg-gold-500 hover:bg-gold-400 text-brand-950 font-bold px-6 py-3 rounded-xl transition-colors"
            >
              Ler hoje
              <span>→</span>
            </Link>
          </div>

          {/* Day navigator */}
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <h2 className="font-bold text-gray-900 mb-4">Ir para um dia específico</h2>
            <div className="flex gap-3">
              <input
                type="number"
                min={1}
                max={365}
                placeholder="Ex: 42"
                className="flex-1 px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500"
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    const val = (e.target as HTMLInputElement).value;
                    if (val) window.location.href = `/plano-de-leitura/${val}`;
                  }
                }}
              />
              <button
                className="px-4 py-2 bg-brand-600 text-white rounded-xl font-medium hover:bg-brand-700 transition-colors"
                onClick={(e) => {
                  const input = (e.currentTarget.previousSibling as HTMLInputElement);
                  if (input.value) window.location.href = `/plano-de-leitura/${input.value}`;
                }}
              >
                Ir
              </button>
            </div>
          </div>
        </>
      ) : (
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 text-center">
          <div className="text-5xl mb-4">📅</div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Comece sua jornada de 365 dias</h2>
          <p className="text-gray-500 mb-6">
            Um capítulo por dia. Em um ano, você terá percorrido toda a Bíblia em ordem cronológica.
          </p>
          <button
            onClick={startPlan}
            disabled={starting}
            className="px-8 py-3 bg-brand-600 hover:bg-brand-700 text-white font-bold rounded-xl transition-colors disabled:opacity-50"
          >
            {starting ? "Iniciando..." : "Começar o plano"}
          </button>
        </div>
      )}
    </div>
  );
}
