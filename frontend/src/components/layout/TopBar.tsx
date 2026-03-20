"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import api from "@/lib/api";
import { useAuthStore } from "@/store/authStore";

export default function TopBar() {
  const router = useRouter();
  const { user, logout } = useAuthStore();
  const [search, setSearch] = useState("");

  async function handleLogout() {
    try {
      await api.post("/api/auth/logout");
    } catch {
      // ignore
    }
    logout();
    router.push("/");
  }

  function handleSearch(e: React.FormEvent) {
    e.preventDefault();
    if (search.trim()) {
      router.push(`/busca?q=${encodeURIComponent(search.trim())}`);
    }
  }

  return (
    <header className="bg-white border-b border-gray-100 px-6 py-4 flex items-center justify-between gap-4">
      {/* Search */}
      <form onSubmit={handleSearch} className="flex-1 max-w-md">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">🔍</span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar histórias, personagens..."
            className="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
          />
        </div>
      </form>

      {/* User menu */}
      <div className="flex items-center gap-4">
        {user && (
          <span className="text-sm text-gray-500 hidden sm:block">
            Olá, <span className="font-medium text-gray-700">{user.full_name.split(" ")[0]}</span>
          </span>
        )}
        <button
          onClick={handleLogout}
          className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
        >
          Sair
        </button>
      </div>
    </header>
  );
}
