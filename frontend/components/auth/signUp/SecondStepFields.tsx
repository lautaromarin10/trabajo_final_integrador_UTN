import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { REGEX_EMAIL, REGEX_PASSWORD } from "@/utils/auth/regex";
import { Eye, EyeClosed } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { FormState, UseFormGetValues, UseFormRegister } from "react-hook-form";
import { viewPasswordField, SignUpField } from "@/hooks/auth/useSignUpForm";

interface SecondStepFieldsProps {
  register: UseFormRegister<SignUpField>;
  getValues: UseFormGetValues<SignUpField>;
  formState: FormState<SignUpField>;
  handleViewPassword: (field: viewPasswordField) => void;
  viewPassword: Record<string, boolean>;
}

export const SecondStepFields = ({
  register,
  getValues,
  formState,
  handleViewPassword,
  viewPassword,
}: SecondStepFieldsProps) => {
  const { errors } = formState;

  return (
    <FieldGroup className="w-full">
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
                message:
                  "Usá al menos 8 caracteres, una mayúscula y un símbolo",
              },
            })}
            aria-invalid={errors.password ? true : false}
            type={viewPassword["password"] ? "text" : "password"}
            placeholder="Contraseña"
            className="pr-10"
          />
          <div className={"absolute right-0 h-full flex items-center"}>
            <Button
              type="button"
              size={"icon"}
              variant={"ghost"}
              onClick={() => handleViewPassword("password")}
            >
              {viewPassword["password"] ? <Eye /> : <EyeClosed />}
            </Button>
          </div>
        </div>
        <FieldError>{errors.password?.message}</FieldError>
      </Field>
      <Field data-invalid={errors.password_validate ? true : false}>
        <FieldLabel>Confirmar contraseña</FieldLabel>
        <div className="w-full flex group relative">
          <Input
            {...register("password_validate", {
              required: "Confirmá tu contraseña",
              validate: (value) =>
                value === getValues("password") ||
                "Las contraseñas no coinciden",
            })}
            aria-invalid={Boolean(errors.password_validate)}
            type={viewPassword["password_validate"] ? "text" : "password"}
            placeholder="Confirmá tu contraseña"
            className="pr-10"
          />
          <div className={"absolute right-0 h-full flex items-center"}>
            <Button
              type="button"
              size={"icon"}
              variant={"ghost"}
              onClick={() => handleViewPassword("password_validate")}
            >
              {viewPassword["password_validate"] ? <Eye /> : <EyeClosed />}
            </Button>
          </div>
        </div>
        <FieldError>{errors.password_validate?.message}</FieldError>
      </Field>
    </FieldGroup>
  );
};
