const features = [
  {
    icon: "📖",
    title: "Bíblia em Ordem Cronológica",
    description:
      "Todas as histórias reorganizadas na sequência em que aconteceram. Da Criação ao Apocalipse, cada evento no seu contexto histórico correto.",
  },
  {
    icon: "🗺️",
    title: "Linha do Tempo Interativa",
    description:
      "Visualize 4.000 anos de história bíblica em uma timeline interativa. Veja onde cada personagem e evento se encaixam no grande quadro.",
  },
  {
    icon: "📅",
    title: "Plano de Leitura 365 Dias",
    description:
      "Um capítulo por dia. Acompanhe seu progresso, mantenha sua sequência de dias e chegue ao fim da Bíblia em um ano.",
  },
  {
    icon: "👥",
    title: "Galeria de Personagens",
    description:
      "Conheça cada personagem bíblico: sua história, sua época, seu papel na grande narrativa. De Adão a João, todos estão aqui.",
  },
  {
    icon: "🔍",
    title: "Busca Inteligente",
    description:
      "Procure qualquer coisa: uma história, um personagem, um tema. Nossa busca entende português e encontra o que você precisa.",
  },
  {
    icon: "✍️",
    title: "Anotações Pessoais",
    description:
      "Registre seus pensamentos e reflexões enquanto lê. Suas anotações ficam salvas e organizadas por história e personagem.",
  },
];

export default function FeaturesSection() {
  return (
    <section id="funcionalidades" className="py-24 bg-gray-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Tudo que você precisa para entender a Bíblia
          </h2>
          <p className="text-xl text-gray-500 max-w-2xl mx-auto">
            O Maka foi feito para ser simples. Seja você quem está lendo a Bíblia pela primeira vez
            ou quem quer aprofundar seu entendimento.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow border border-gray-100"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
              <p className="text-gray-500 leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
