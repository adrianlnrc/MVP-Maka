"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import type { CharacterBrief } from "@/types/content";

export default function PersonagensPage() {
  const [characters, setCharacters] = useState<CharacterBrief[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    api.get(`/api/characters?page=${page}&page_size=24`)
      .then((r) => {
        setCharacters(r.data.items);
        setTotal(r.data.total);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [page]);

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Personagens Bíblicos</h1>
        <p className="text-gray-500 mt-1">
          Conheça quem viveu, amou e lutou nas páginas das Escrituras.
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {characters.map((char) => (
              <Link
                key={char.id}
                href={`/personagens/${char.slug}`}
                className="bg-white rounded-2xl p-5 shadow-sm border border-gray-100 hover:shadow-md hover:border-brand-200 transition-all text-center"
              >
                <div className="w-14 h-14 bg-brand-100 rounded-full flex items-center justify-center text-brand-700 text-xl font-bold mx-auto mb-3">
                  {char.name.charAt(0)}
                </div>
                <p className="font-semibold text-gray-900 text-sm">{char.name}</p>
                <p className="text-xs text-gray-400 mt-0.5">{char.role}</p>
              </Link>
            ))}
          </div>

          {total > 24 && (
            <div className="flex justify-center gap-3 mt-8">
              <button
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
                className="px-4 py-2 border border-gray-200 rounded-xl disabled:opacity-40 hover:bg-gray-50 transition-colors"
              >
                ← Anterior
              </button>
              <span className="px-4 py-2 text-gray-500 text-sm">
                Página {page} · {total} personagens
              </span>
              <button
                disabled={characters.length < 24}
                onClick={() => setPage((p) => p + 1)}
                className="px-4 py-2 border border-gray-200 rounded-xl disabled:opacity-40 hover:bg-gray-50 transition-colors"
              >
                Próxima →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
