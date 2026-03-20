"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import type { StoryBrief, CharacterBrief } from "@/types/content";
import { Suspense } from "react";

function BuscaContent() {
  const params = useSearchParams();
  const q = params.get("q") || "";
  const [query, setQuery] = useState(q);
  const [results, setResults] = useState<{ stories: StoryBrief[]; characters: CharacterBrief[] }>({
    stories: [],
    characters: [],
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!q) return;
    setQuery(q);
    setLoading(true);
    api.get(`/api/search?q=${encodeURIComponent(q)}`)
      .then((r) => setResults(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [q]);

  const total = results.stories.length + results.characters.length;

  return (
    <div className="max-w-3xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Busca</h1>
        {q && <p className="text-gray-500 mt-1">Resultados para: <strong>"{q}"</strong></p>}
      </div>

      {/* Search bar */}
      <form className="mb-8" action="/busca" method="get">
        <input
          type="text"
          name="q"
          defaultValue={q}
          placeholder="Buscar histórias, personagens..."
          className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 text-lg"
        />
      </form>

      {loading && <p className="text-gray-400">Buscando...</p>}

      {!loading && q && total === 0 && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-5xl mb-4">🔍</div>
          <p>Nenhum resultado encontrado para "{q}".</p>
        </div>
      )}

      {results.stories.length > 0 && (
        <section className="mb-8">
          <h2 className="font-bold text-gray-700 text-sm uppercase tracking-wide mb-3">
            Histórias ({results.stories.length})
          </h2>
          <div className="space-y-3">
            {results.stories.map((story) => (
              <Link
                key={story.id}
                href={`/cronologia/${story.era_id}/${story.slug}`}
                className="block bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md hover:border-brand-200 transition-all"
              >
                <p className="font-semibold text-gray-900">{story.title}</p>
                <p className="text-sm text-gray-500 mt-1 line-clamp-2">{story.summary}</p>
                <div className="flex gap-2 mt-2">
                  {story.themes.slice(0, 3).map((t) => (
                    <span key={t} className="text-xs bg-brand-50 text-brand-700 px-2 py-0.5 rounded-full">
                      {t}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      {results.characters.length > 0 && (
        <section>
          <h2 className="font-bold text-gray-700 text-sm uppercase tracking-wide mb-3">
            Personagens ({results.characters.length})
          </h2>
          <div className="grid grid-cols-2 gap-3">
            {results.characters.map((char) => (
              <Link
                key={char.id}
                href={`/personagens/${char.slug}`}
                className="bg-white rounded-xl p-4 border border-gray-100 hover:shadow-md hover:border-brand-200 transition-all"
              >
                <p className="font-semibold text-gray-900">{char.name}</p>
                <p className="text-sm text-gray-400 mt-0.5">{char.role}</p>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

export default function BuscaPage() {
  return (
    <Suspense fallback={<div className="animate-pulse h-64 bg-gray-200 rounded-2xl" />}>
      <BuscaContent />
    </Suspense>
  );
}
