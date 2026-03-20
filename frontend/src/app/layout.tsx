import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Maka — Bíblia Cronológica",
  description:
    "Entenda a Bíblia como nunca antes — da Criação ao Apocalipse em ordem cronológica. Um lugar fácil para se conectar com Deus.",
  keywords: ["Bíblia", "estudo bíblico", "cronológico", "fé", "Jesus", "Deus"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="antialiased">{children}</body>
    </html>
  );
}
