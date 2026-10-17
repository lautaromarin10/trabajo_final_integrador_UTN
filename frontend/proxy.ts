import { NextRequest, NextResponse } from "next/server";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;

type CurrentUser = {
  role: "admin" | "user";
};

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isAdminRoute = pathname.startsWith("/admin");
  const isUserRoute = pathname.startsWith("/user");
  const isAuthPage = pathname === "/auth/signin" || pathname === "/auth/signup";
  const isHomePage = pathname === "/";
  const token = request.cookies.get("access_token");

  if (!token) {
    return isAdminRoute || isUserRoute
      ? NextResponse.redirect(new URL("/auth/signin", request.url))
      : NextResponse.next();
  }

  if (!backendUrl) {
    console.error("NEXT_PUBLIC_BACKEND_URL no está configurada");
    return isAdminRoute || isUserRoute
      ? NextResponse.redirect(new URL("/auth/signin", request.url))
      : NextResponse.next();
  }

  let profileResponse: Response;
  try {
    profileResponse = await fetch(`${backendUrl}/auth/me`, {
      headers: { cookie: request.headers.get("cookie") ?? "" },
      cache: "no-store",
    });
  } catch (error) {
    console.error("No se pudo verificar la sesión con el backend", error);
    return isAdminRoute || isUserRoute
      ? NextResponse.redirect(new URL("/auth/signin", request.url))
      : NextResponse.next();
  }

  if (!profileResponse.ok) {
    if (isAdminRoute || isUserRoute) {
      const redirect = NextResponse.redirect(
        new URL("/auth/signin", request.url),
      );
      redirect.cookies.delete("access_token");
      return redirect;
    }
    return NextResponse.next();
  }

  const user = (await profileResponse.json()) as CurrentUser;
  const dashboard = user.role === "admin" ? "/admin" : "/user";

  if (isHomePage || isAuthPage) {
    return NextResponse.redirect(new URL(dashboard, request.url));
  }

  if (isAdminRoute && user.role !== "admin") {
    return NextResponse.redirect(new URL("/user", request.url));
  }

  if (isUserRoute && user.role !== "user") {
    return NextResponse.redirect(new URL("/admin", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/admin/:path*", "/user/:path*", "/auth/signin", "/auth/signup"],
};
