"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/inicio", icon: "🏠", label: "Início" },
  { href: "/cronologia", icon: "📖", label: "Cronologia" },
  { href: "/personagens", icon: "👥", label: "Personagens" },
  { href: "/linha-do-tempo", icon: "🗺️", label: "Linha do Tempo" },
  { href: "/plano-de-leitura", icon: "📅", label: "Plano de Leitura" },
  { href: "/busca", icon: "🔍", label: "Busca" },
  { href: "/perfil", icon: "⚙️", label: "Perfil" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex flex-col w-64 bg-brand-950 text-white h-screen sticky top-0">
      <div className="p-6 border-b border-brand-800">
        <Link href="/inicio" className="font-bold text-xl text-white">
          Maka
        </Link>
        <p className="text-brand-400 text-xs mt-0.5">Bíblia Cronológica</p>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {nav.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors",
                active
                  ? "bg-brand-700 text-white"
                  : "text-brand-300 hover:bg-brand-800 hover:text-white"
              )}
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
