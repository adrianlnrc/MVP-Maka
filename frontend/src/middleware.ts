import { NextRequest, NextResponse } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/cadastro", "/recuperar-senha"];
const APP_PATHS = ["/inicio", "/cronologia", "/personagens", "/linha-do-tempo", "/plano-de-leitura", "/busca", "/perfil"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isAppPath = APP_PATHS.some((p) => pathname.startsWith(p));
  const hasRefreshCookie = request.cookies.has("maka_auth");

  if (isAppPath && !hasRefreshCookie) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
