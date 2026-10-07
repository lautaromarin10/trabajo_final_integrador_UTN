import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";
import { cn } from "@/lib/utils";
import Header from "@/components/globals/Header";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Reservas | UTN",
  description: "Proyecto final integrador sobre reservas hoteleras",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="es"
      className={cn("h-full", "antialiased", "font-sans", inter.variable)}
    >
      <body className="">
        <Header />
        <main className="translate-y-20">{children}</main>
      </body>
    </html>
  );
}
