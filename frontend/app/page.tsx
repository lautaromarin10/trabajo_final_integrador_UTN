import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Stars } from "lucide-react";
import Image from "next/image";

export default function Home() {
  return (
    <section className="relative flex min-h-[calc(100svh-5rem)] flex-col items-center">
      <div className="container mx-auto flex items-center justify-center py-12 text-center [@media(orientation:landscape)_and_(max-height:500px)]:py-2">
        <div className="flex flex-col items-center text-center max-w-prose">
          <Badge variant={"secondary"} className="mb-2">
            <Stars className="text-yellow-700" /> 4.8 en Google Reviews
          </Badge>
          <h1 className="title-xxl xl:text-5xl mb-2 text-balance [@media(orientation:landscape)_and_(max-height:500px)]:text-[clamp(1.5rem,4vw,1.875rem)]">
            Tus próximas vacaciones son en Lumatha Hotel
          </h1>
          <p className="text-pretty">
            Descansá, disfrutá y dejá que nosotros nos ocupemos del resto.
          </p>
          <p className="text-pretty">
            Reservá tu estadía y empezá a planificar tu próxima escapada.
          </p>
          <div className="mt-4 flex flex-row items-center justify-center flex-wrap gap-2">
            <Button>Iniciar sesión</Button>
            <Button variant={"outline"}>Registrarse ahora</Button>
          </div>
        </div>
      </div>
      <div className="relative mt-auto min-h-[clamp(4rem,18svh,7rem)] w-full max-w-[1920px] flex-1 overflow-hidden">
        <Image
          src="/alaverdi.jpg"
          fill
          sizes="(min-width: 1920px) 1920px, 100vw"
          alt="Hero Image"
          loading="eager"
          className="object-cover"
        />
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-b from-background via-background/70 to-transparent"
        />
      </div>
    </section>
  );
}
