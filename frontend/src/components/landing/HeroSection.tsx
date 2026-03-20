import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-brand-950 via-brand-900 to-brand-800 text-white">
      {/* Background decoration */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-10 w-72 h-72 rounded-full bg-brand-400 blur-3xl" />
        <div className="absolute bottom-20 right-10 w-96 h-96 rounded-full bg-gold-400 blur-3xl" />
      </div>

      <div className="relative max-w-5xl mx-auto px-6 py-24 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-white/10 border border-white/20 rounded-full px-4 py-1.5 text-sm text-brand-200 mb-8">
          <span className="w-2 h-2 bg-gold-400 rounded-full animate-pulse" />
          Da Criação ao Apocalipse
        </div>

        {/* Headline */}
        <h1 className="text-5xl md:text-7xl font-bold leading-tight mb-6">
          Entenda a Bíblia{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-gold-400 to-gold-500">
            como ela aconteceu
          </span>
        </h1>

        {/* Sub */}
        <p className="text-xl md:text-2xl text-brand-200 max-w-3xl mx-auto mb-10 leading-relaxed">
          O <strong className="text-white">Maka</strong> reorganiza todas as histórias das Escrituras na
          sequência cronológica correta. Acompanhe cada personagem, cada evento
          e veja como tudo se conecta — do início ao fim.
        </p>

        {/* Problem statement */}
        <p className="text-brand-300 mb-10">
          Você já tentou ler a Bíblia e se perdeu no meio do caminho?{" "}
          <span className="text-white font-medium">Você não está sozinho.</span>{" "}
          Sem o contexto cronológico, a Bíblia parece um quebra-cabeça sem ordem.
        </p>

        {/* CTA */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/cadastro"
            className="inline-flex items-center justify-center px-8 py-4 bg-gold-500 hover:bg-gold-400 text-brand-950 font-bold rounded-xl text-lg transition-all transform hover:scale-105 shadow-lg shadow-gold-500/30"
          >
            Começar agora — é grátis
          </Link>
          <Link
            href="#funcionalidades"
            className="inline-flex items-center justify-center px-8 py-4 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-semibold rounded-xl text-lg transition-all"
          >
            Ver como funciona
          </Link>
        </div>

        {/* Social proof */}
        <div className="mt-16 flex flex-wrap justify-center gap-8 text-brand-300 text-sm">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-white">12</span>
            <span>Épocas bíblicas</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-white">200+</span>
            <span>Histórias em português</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-white">365</span>
            <span>Dias de leitura</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-white">100%</span>
            <span>Gratuito para começar</span>
          </div>
        </div>
      </div>
    </section>
  );
}
