import Link from "next/link";

export default function PricingSection() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-900 mb-4">
          Comece gratuitamente hoje
        </h2>
        <p className="text-xl text-gray-500 mb-12">
          Crie sua conta e explore a Bíblia em ordem cronológica sem pagar nada.
        </p>

        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          {/* Free */}
          <div className="border-2 border-gray-200 rounded-2xl p-8 text-left">
            <h3 className="text-xl font-bold text-gray-900 mb-2">Gratuito</h3>
            <p className="text-4xl font-bold text-gray-900 mb-1">R$ 0</p>
            <p className="text-gray-500 mb-6">para sempre</p>
            <ul className="space-y-3 text-gray-600 mb-8">
              {[
                "Acesso às primeiras 20 histórias",
                "Linha do tempo (épocas principais)",
                "Plano de leitura — 30 dias",
                "Galeria de personagens básica",
              ].map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="text-green-500">✓</span>
                  {item}
                </li>
              ))}
            </ul>
            <Link
              href="/cadastro"
              className="block text-center px-6 py-3 border-2 border-brand-600 text-brand-600 font-semibold rounded-xl hover:bg-brand-50 transition-colors"
            >
              Criar conta grátis
            </Link>
          </div>

          {/* Pro */}
          <div className="bg-brand-900 border-2 border-brand-600 rounded-2xl p-8 text-left relative overflow-hidden">
            <div className="absolute top-4 right-4 bg-gold-500 text-brand-950 text-xs font-bold px-2 py-1 rounded-full">
              POPULAR
            </div>
            <h3 className="text-xl font-bold text-white mb-2">Completo</h3>
            <p className="text-4xl font-bold text-white mb-1">R$ 47,90</p>
            <p className="text-brand-300 mb-6">pagamento único · acesso vitalício</p>
            <ul className="space-y-3 text-brand-200 mb-8">
              {[
                "200+ histórias completas",
                "Linha do tempo interativa completa",
                "Plano de leitura 365 dias",
                "Galeria completa de personagens",
                "Busca inteligente",
                "Anotações pessoais ilimitadas",
                "Atualizações gratuitas para sempre",
              ].map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="text-gold-400">✓</span>
                  {item}
                </li>
              ))}
            </ul>
            <Link
              href="/cadastro"
              className="block text-center px-6 py-3 bg-gold-500 hover:bg-gold-400 text-brand-950 font-bold rounded-xl transition-colors"
            >
              Garantir acesso completo
            </Link>
            <p className="text-center text-brand-400 text-xs mt-3">
              Garantia de 7 dias. Sem perguntas.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
