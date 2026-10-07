import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Stars } from "lucide-react";
import Image from "next/image";

export default function Home() {
  return (
    <section className="min-h-[calc(100vh-5rem)] max-w-[1920px] flex flex-col justify-between items-center">
      <div className="flex items-center justify-center container mx-auto mt-30">
        <div className="flex flex-col items-center text-center max-w-prose">
          <Badge variant={"secondary"} className="mb-2">
            <Stars className="text-yellow-700" /> 4.8 en Google Reviews
          </Badge>
          <h1 className="title-xxl xl:text-5xl mb-2 text-balance">
            Tus próximas vacaciones son en Lumatha Hotel
          </h1>
          <p className="text-pretty">
            Descansá, disfrutá y dejá que nosotros nos ocupemos del resto.
          </p>
          <p className="text-pretty">
            Reservá tu estadía y empezá a planificar tu próxima escapada.
          </p>
          <div className="mt-4 flex flex-row flex-wrap gap-2">
            <Button>Iniciar sesión</Button>
            <Button variant={"outline"}>Registrarse ahora</Button>
          </div>
        </div>
      </div>
      <Image
        src={"/alaverdi.jpg"}
        width={1920}
        height={1080}
        alt="Alaverdi Hero Image"
        loading="eager"
        className="mt-8 mask-t-from-85 object-cover min-h-100 sm:max-h-140 sm:min-h-150"
      />
    </section>
  );
}
