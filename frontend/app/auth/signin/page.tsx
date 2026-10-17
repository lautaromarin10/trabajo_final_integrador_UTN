import SignInForm from "@/components/auth/SignInForm";
import Logo from "@/components/globals/Logo";
import Link from "next/link";

const Page = () => {
  return (
    <section className="container flex-col min-h-screen-and-header mx-auto flex justify-center items-center">
      <div className="mb-6 flex items-center flex-col">
        <Logo />
        <h1 className="title-lg">Iniciar sesión</h1>
      </div>
      <div className="flex flex-col items-center border-2 border-muted rounded-2xl min-h-fit w-full max-w-sm p-4 sm:p-8">
        <SignInForm />
        <div className="mt-4">
          <p className="text-sm">
            ¿No tienes una cuenta?{" "}
            <Link href={"/auth/signup"} className="text-black!">
              Registrarse
            </Link>
          </p>
        </div>
      </div>
    </section>
  );
};

export default Page;
