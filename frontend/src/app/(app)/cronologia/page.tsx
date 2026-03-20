import Link from "next/link";
import type { Era } from "@/types/content";

async function getEras(): Promise<Era[]> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/eras`, {
      cache: "no-store",
    });
    if (!res.ok) return [];
    return res.json();
  } catch {
    return [];
  }
}

export default async function CronologiaPage() {
  const eras = await getEras();

  return (
    <div className="max-w-5xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Cronologia Bíblica</h1>
        <p className="text-gray-500 mt-2">
          Da Criação ao Apocalipse — todas as histórias na ordem em que aconteceram.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {eras.map((era) => (
          <Link
            key={era.slug}
            href={`/cronologia/${era.slug}`}
            className="group bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition-all"
          >
            {/* Color header */}
            <div
              className="h-3 w-full"
              style={{ backgroundColor: era.color_hex }}
            />
            <div className="p-6">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide">
                    Época {era.order_index}
                  </p>
                  <h2 className="text-xl font-bold text-gray-900 mt-1 group-hover:text-brand-700 transition-colors">
                    {era.name}
                  </h2>
                </div>
                <span
                  className="text-xs px-2 py-1 rounded-full text-white font-medium"
                  style={{ backgroundColor: era.color_hex }}
                >
                  {era.story_count} hist.
                </span>
              </div>

              <p className="text-gray-500 text-sm leading-relaxed line-clamp-3 mb-4">
                {era.description}
              </p>

              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>{era.approx_date_start}</span>
                <span>→</span>
                <span>{era.approx_date_end}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {eras.length === 0 && (
        <div className="text-center py-16 text-gray-400">
          <div className="text-5xl mb-4">📖</div>
          <p>Nenhuma época encontrada. O banco de dados pode estar sendo populado.</p>
        </div>
      )}
    </div>
  );
}
