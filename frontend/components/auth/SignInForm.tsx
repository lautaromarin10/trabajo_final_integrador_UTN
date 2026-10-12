"use client";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import useSignInForm from "@/hooks/auth/useSignInForm";
import { REGEX_EMAIL, REGEX_PASSWORD } from "@/utils/auth/regex";
import { Eye, EyeClosed, InfoIcon } from "lucide-react";
import { Alert, AlertDescription } from "../ui/alert";

const SignInForm = () => {
  const {
    viewPassword,
    handleViewPassword,
    handleSubmit,
    register,
    formState: { errors },
    onSubmit,
    signInError,
  } = useSignInForm();

  return (
    <>
      {signInError && (
        <Alert variant={"destructive"} className="mb-4">
          <InfoIcon />
          <AlertDescription>{signInError}</AlertDescription>
        </Alert>
      )}
      <form className="w-full h-full" onSubmit={handleSubmit(onSubmit)}>
        <FieldGroup className="gap-4">
          <Field data-invalid={errors.email ? true : false}>
            <FieldLabel>Correo electrónico</FieldLabel>
            <Input
              {...register("email", {
                required: "El email es obligatorio",
                pattern: {
                  value: REGEX_EMAIL,
                  message: "Ingresá un email valido",
                },
              })}
              aria-invalid={errors.email ? true : false}
              type="email"
              placeholder="Tu correo electrónico"
            />
            <FieldError>{errors.email?.message}</FieldError>
          </Field>
          <Field data-invalid={errors.password ? true : false}>
            <FieldLabel>Contraseña</FieldLabel>
            <div className="w-full flex group relative">
              <Input
                {...register("password", {
                  required: "La contraseña es requerida",
                  pattern: {
                    value: REGEX_PASSWORD,
                    message: "Ingresá una contraseña valida",
                  },
                })}
                aria-invalid={errors.password ? true : false}
                type={viewPassword ? "text" : "password"}
                placeholder="Contraseña"
                className="pr-10"
              />
              <div className={"absolute right-0 h-full flex items-center"}>
                <Button
                  size={"icon"}
                  variant={"ghost"}
                  onClick={handleViewPassword}
                >
                  {viewPassword ? <Eye /> : <EyeClosed />}
                </Button>
              </div>
            </div>
            <FieldError>{errors.password?.message}</FieldError>
          </Field>
        </FieldGroup>
        <div className="mt-4 w-full">
          <Button className={"w-full"} type="submit">
            Continuar
          </Button>
        </div>
      </form>
    </>
  );
};

export default SignInForm;
