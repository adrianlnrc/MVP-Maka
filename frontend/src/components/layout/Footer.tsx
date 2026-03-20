import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-12">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div>
            <p className="text-white font-bold text-xl mb-1">Maka</p>
            <p className="text-sm">Bíblia Cronológica</p>
          </div>
          <nav className="flex gap-6 text-sm">
            <Link href="/" className="hover:text-white transition-colors">Início</Link>
            <Link href="/login" className="hover:text-white transition-colors">Entrar</Link>
            <Link href="/cadastro" className="hover:text-white transition-colors">Criar conta</Link>
          </nav>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
          <p>© {new Date().getFullYear()} Maka. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}
