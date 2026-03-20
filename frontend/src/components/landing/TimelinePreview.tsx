const eras = [
  { name: "Criação", date: "~4000 a.C.", color: "#7c3aed" },
  { name: "Patriarcas", date: "~2000 a.C.", color: "#d97706" },
  { name: "Êxodo", date: "~1446 a.C.", color: "#b45309" },
  { name: "Conquista", date: "~1400 a.C.", color: "#15803d" },
  { name: "Juízes", date: "~1350 a.C.", color: "#0369a1" },
  { name: "Reino", date: "~1050 a.C.", color: "#dc2626" },
  { name: "Exílio", date: "586 a.C.", color: "#475569" },
  { name: "Retorno", date: "538 a.C.", color: "#0891b2" },
  { name: "Jesus", date: "~4 a.C.", color: "#eab308" },
  { name: "Igreja", date: "30 d.C.", color: "#0d9488" },
];

export default function TimelinePreview() {
  return (
    <section className="py-24 bg-white overflow-hidden">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            4.000 anos de história em uma linha do tempo
          </h2>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto">
            Visualize como todos os eventos se conectam — da Criação ao Apocalipse.
          </p>
        </div>

        {/* Timeline strip */}
        <div className="relative">
          {/* Central line */}
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gray-200 -translate-y-1/2" />

          <div className="flex items-center gap-0 overflow-x-auto pb-4">
            {eras.map((era, i) => (
              <div key={era.name} className="flex-shrink-0 flex flex-col items-center relative" style={{ width: "10%" }}>
                {/* Dot */}
                <div
                  className="w-4 h-4 rounded-full border-2 border-white shadow-md z-10 mb-2"
                  style={{ backgroundColor: era.color }}
                />
                {/* Label above for even, below for odd */}
                {i % 2 === 0 ? (
                  <>
                    <div className="text-xs font-semibold text-gray-700 text-center whitespace-nowrap -mt-12 mb-10">{era.name}</div>
                    <div className="text-xs text-gray-400 text-center whitespace-nowrap -mt-10">{era.date}</div>
                  </>
                ) : (
                  <>
                    <div className="text-xs font-semibold text-gray-700 text-center whitespace-nowrap mt-4">{era.name}</div>
                    <div className="text-xs text-gray-400 text-center whitespace-nowrap">{era.date}</div>
                  </>
                )}
              </div>
            ))}
          </div>
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-500 mb-6">
            No Maka, você pode explorar cada época, filtrar por personagem e ver como tudo se conecta.
          </p>
          <a
            href="/cadastro"
            className="inline-flex items-center gap-2 px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white font-semibold rounded-xl transition-colors"
          >
            Explorar a linha do tempo
            <span>→</span>
          </a>
        </div>
      </div>
    </section>
  );
}
