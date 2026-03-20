"use client";

import { useEffect, useState, useRef } from "react";
import api from "@/lib/api";
import type { Era, TimelineEvent } from "@/types/content";

const EVENT_TYPE_COLORS: Record<string, string> = {
  event: "#6366f1",
  birth: "#10b981",
  death: "#6b7280",
  miracle: "#f59e0b",
  war: "#ef4444",
  covenant: "#8b5cf6",
  prophecy: "#3b82f6",
};

export default function LinhaDoTempoPage() {
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [eras, setEras] = useState<Era[]>([]);
  const [selectedEra, setSelectedEra] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{ event: TimelineEvent; x: number; y: number } | null>(null);
  const [loading, setLoading] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function load() {
      const [eventsRes, erasRes] = await Promise.all([
        api.get("/api/timeline"),
        api.get("/api/eras"),
      ]);
      setEvents(eventsRes.data);
      setEras(erasRes.data);
      setLoading(false);
    }
    load();
  }, []);

  const filteredEvents = selectedEra
    ? events.filter((e) => {
        const era = eras.find((er) => er.id === e.era_id);
        return era?.slug === selectedEra;
      })
    : events;

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-48 mb-8" />
        <div className="h-64 bg-gray-200 rounded-2xl" />
      </div>
    );
  }

  const minYear = Math.min(...filteredEvents.map((e) => e.year_approx));
  const maxYear = Math.max(...filteredEvents.map((e) => e.year_approx));
  const range = maxYear - minYear || 1;
  const WIDTH = 3000;

  function yearToX(year: number) {
    return ((year - minYear) / range) * (WIDTH - 100) + 50;
  }

  return (
    <div className="max-w-full">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Linha do Tempo</h1>
        <p className="text-gray-500 mt-1">Explore 4.000+ anos de história bíblica</p>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-3 mb-4 text-xs">
        {Object.entries(EVENT_TYPE_COLORS).map(([type, color]) => (
          <div key={type} className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-gray-500 capitalize">{type}</span>
          </div>
        ))}
      </div>

      {/* Era filters */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button
          onClick={() => setSelectedEra(null)}
          className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
            !selectedEra ? "bg-brand-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
          }`}
        >
          Todas as épocas
        </button>
        {eras.map((era) => (
          <button
            key={era.slug}
            onClick={() => setSelectedEra(era.slug === selectedEra ? null : era.slug)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              selectedEra === era.slug ? "text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
            style={selectedEra === era.slug ? { backgroundColor: era.color_hex } : {}}
          >
            {era.name}
          </button>
        ))}
      </div>

      {/* SVG Timeline */}
      <div
        ref={containerRef}
        className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-x-auto relative"
      >
        <svg width={WIDTH} height={200} className="block">
          {/* Era background bands */}
          {eras
            .filter((era) => !selectedEra || era.slug === selectedEra)
            .map((era) => {
              const eraEvents = filteredEvents.filter((e) => e.era_id === era.id);
              if (eraEvents.length === 0) return null;
              const x1 = yearToX(Math.min(...eraEvents.map((e) => e.year_approx)));
              const x2 = yearToX(Math.max(...eraEvents.map((e) => e.year_approx)));
              return (
                <rect
                  key={era.id}
                  x={x1 - 10}
                  y={70}
                  width={x2 - x1 + 20}
                  height={60}
                  fill={era.color_hex}
                  opacity={0.08}
                  rx={6}
                />
              );
            })}

          {/* Central axis */}
          <line x1={0} y1={100} x2={WIDTH} y2={100} stroke="#e5e7eb" strokeWidth={2} />

          {/* Events */}
          {filteredEvents.map((event, i) => {
            const x = yearToX(event.year_approx);
            const above = i % 2 === 0;
            const color = EVENT_TYPE_COLORS[event.event_type] || "#6366f1";

            return (
              <g
                key={event.id}
                onClick={(e) => {
                  const rect = containerRef.current?.getBoundingClientRect();
                  setTooltip({
                    event,
                    x: e.clientX - (rect?.left || 0),
                    y: e.clientY - (rect?.top || 0),
                  });
                }}
                className="cursor-pointer"
              >
                {/* Connecting line */}
                <line
                  x1={x} y1={100}
                  x2={x} y2={above ? 70 : 130}
                  stroke={color}
                  strokeWidth={1.5}
                  opacity={0.5}
                />
                {/* Dot */}
                <circle
                  cx={x} cy={100}
                  r={5}
                  fill={color}
                  stroke="white"
                  strokeWidth={2}
                />
                {/* Label */}
                <text
                  x={x}
                  y={above ? 60 : 150}
                  textAnchor="middle"
                  fontSize={10}
                  fill="#374151"
                  className="select-none"
                >
                  {event.title.length > 20 ? event.title.slice(0, 20) + "…" : event.title}
                </text>
                <text
                  x={x}
                  y={above ? 48 : 162}
                  textAnchor="middle"
                  fontSize={9}
                  fill="#9ca3af"
                  className="select-none"
                >
                  {event.year_display}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Tooltip */}
        {tooltip && (
          <div
            className="absolute bg-white border border-gray-200 rounded-xl shadow-lg p-4 max-w-xs z-10 pointer-events-none"
            style={{ left: tooltip.x + 10, top: tooltip.y - 60 }}
            onClick={() => setTooltip(null)}
          >
            <p className="font-bold text-gray-900 text-sm mb-1">{tooltip.event.title}</p>
            <p className="text-xs text-brand-600 mb-2">{tooltip.event.year_display}</p>
            <p className="text-xs text-gray-500 leading-relaxed">{tooltip.event.description}</p>
            <button
              className="text-xs text-gray-400 mt-2 hover:text-gray-600"
              onClick={() => setTooltip(null)}
            >
              ✕ fechar
            </button>
          </div>
        )}
      </div>

      <p className="text-xs text-gray-400 mt-3 text-center">
        Clique em um evento para ver detalhes. Role horizontalmente para explorar toda a linha do tempo.
      </p>
    </div>
  );
}
