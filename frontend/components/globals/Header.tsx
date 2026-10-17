"use client";

import Logo from "./Logo";
import { usePathname } from "next/navigation";
import Logout from "./Logout";

const Header = () => {
  const pathname = usePathname();
  const isAuthenticatedRoute =
    pathname.startsWith("/admin") || pathname.startsWith("/user");

  return (
    <header className="bg-transparent sticky top-0 w-screen z-90">
      <div className="container h-20 mx-auto flex items-center justify-between">
        <Logo />
        {isAuthenticatedRoute && (
          <nav aria-label="Sesión">
            <Logout />
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
