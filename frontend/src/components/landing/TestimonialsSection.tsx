const testimonials = [
  {
    name: "Ana Paula M.",
    location: "São Paulo, SP",
    text: "Tentei ler a Bíblia inteira três vezes e sempre desisti no Levítico. Com o Maka, finalmente entendi o contexto de cada passagem. Nunca fui tão longe!",
    rating: 5,
  },
  {
    name: "Carlos Eduardo",
    location: "Belo Horizonte, MG",
    text: "A linha do tempo interativa é incrível. Ver como os profetas e os reis viveram no mesmo período mudou completamente minha compreensão do Antigo Testamento.",
    rating: 5,
  },
  {
    name: "Pastora Renata",
    location: "Curitiba, PR",
    text: "Recomendo para toda a minha congregação. O Maka é especialmente útil para novos convertidos que precisam de contexto histórico para entender a Bíblia.",
    rating: 5,
  },
  {
    name: "Marcos Antônio",
    location: "Recife, PE",
    text: "Nunca fui de ler muito, mas o Maka tornou a Bíblia acessível para mim. As histórias em português simples fazem toda a diferença.",
    rating: 5,
  },
  {
    name: "Lucia Fernanda",
    location: "Porto Alegre, RS",
    text: "Completei o plano de 365 dias! Nunca imaginei que iria conseguir. A funcionalidade de sequência de dias me motivou a não perder um dia.",
    rating: 5,
  },
  {
    name: "José Henrique",
    location: "Fortaleza, CE",
    text: "Uso o Maka para preparar minhas lições de escola dominical. A galeria de personagens e as referências bíblicas facilitam demais o preparo.",
    rating: 5,
  },
];

export default function TestimonialsSection() {
  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            O que as pessoas estão dizendo
          </h2>
          <p className="text-xl text-gray-500">
            Milhares de brasileiros já transformaram sua leitura bíblica com o Maka.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((t) => (
            <div
              key={t.name}
              className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100"
            >
              <div className="flex gap-1 mb-4">
                {Array.from({ length: t.rating }).map((_, i) => (
                  <span key={i} className="text-gold-500 text-lg">★</span>
                ))}
              </div>
              <p className="text-gray-700 mb-6 leading-relaxed italic">"{t.text}"</p>
              <div>
                <p className="font-semibold text-gray-900">{t.name}</p>
                <p className="text-sm text-gray-400">{t.location}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
