"use client";

import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldDescription,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { SignUpField } from "@/hooks/auth/useSignUpForm";
import type { Control, FormState, UseFormRegister } from "react-hook-form";
import { Controller } from "react-hook-form";
import { format, startOfDay, subYears } from "date-fns";
import { es } from "date-fns/locale";
import { CalendarDays } from "lucide-react";
import { useState } from "react";
import countries from "i18n-iso-countries";
import spanishLocale from "i18n-iso-countries/langs/es.json";
import { Calendar } from "@/components/ui/calendar";

countries.registerLocale(spanishLocale);

const nationalityOptions = Object.values(countries.getNames("es")).sort(
  (first, second) => first.localeCompare(second, "es"),
);

interface FirstStepFieldsProps {
  register: UseFormRegister<SignUpField>;
  control: Control<SignUpField>;
  formState: FormState<SignUpField>;
}

export const FirstStepFields = ({
  register,
  control,
  formState,
}: FirstStepFieldsProps) => {
  const { errors } = formState;
  const [datePickerOpen, setDatePickerOpen] = useState(false);
  const latestAllowedBirthDate = startOfDay(subYears(new Date(), 18));

  return (
    <FieldGroup className="w-full">
      <Field data-invalid={Boolean(errors.nombre)}>
        <FieldLabel htmlFor="nombre">Nombre</FieldLabel>
        <Input
          {...register("nombre", { required: "El nombre es obligatorio" })}
          id="nombre"
          aria-invalid={Boolean(errors.nombre)}
          placeholder="Tu nombre"
        />
        <FieldError>{errors.nombre?.message}</FieldError>
      </Field>

      <Field data-invalid={Boolean(errors.apellido)}>
        <FieldLabel htmlFor="apellido">Apellido</FieldLabel>
        <Input
          {...register("apellido", { required: "El apellido es obligatorio" })}
          id="apellido"
          aria-invalid={Boolean(errors.apellido)}
          placeholder="Tu apellido"
        />
        <FieldError>{errors.apellido?.message}</FieldError>
      </Field>

      <Field data-invalid={Boolean(errors.tipo_documento)}>
        <FieldLabel htmlFor="tipo_documento">Tipo de documento</FieldLabel>
        <Input
          {...register("tipo_documento", {
            required: "El tipo de documento es obligatorio",
          })}
          id="tipo_documento"
          aria-invalid={Boolean(errors.tipo_documento)}
          placeholder="Por ejemplo, DNI"
        />
        <FieldError>{errors.tipo_documento?.message}</FieldError>
      </Field>

      <Field data-invalid={Boolean(errors.numero_documento)}>
        <FieldLabel htmlFor="numero_documento">Número de documento</FieldLabel>
        <Input
          {...register("numero_documento", {
            required: "El número de documento es obligatorio",
          })}
          id="numero_documento"
          aria-invalid={Boolean(errors.numero_documento)}
          placeholder="Tu número de documento"
        />
        <FieldError>{errors.numero_documento?.message}</FieldError>
      </Field>

      <Controller
        control={control}
        name="fecha_nacimiento"
        rules={{
          required: "La fecha de nacimiento es obligatoria",
          validate: (value) =>
            !value ||
            value <= format(latestAllowedBirthDate, "yyyy-MM-dd") ||
            "Tenés que tener al menos 18 años",
        }}
        render={({ field, fieldState }) => {
          const selectedDate = field.value
            ? new Date(`${field.value}T00:00:00`)
            : undefined;

          return (
            <Field data-invalid={fieldState.invalid}>
              <FieldLabel htmlFor="fecha_nacimiento">
                Fecha de nacimiento
              </FieldLabel>
              <Popover open={datePickerOpen} onOpenChange={setDatePickerOpen}>
                <PopoverTrigger
                  render={
                    <Button
                      type="button"
                      id="fecha_nacimiento"
                      ref={field.ref}
                      onBlur={field.onBlur}
                      variant="outline"
                      aria-invalid={fieldState.invalid}
                      className="w-full justify-start font-normal text-muted-foreground overflow-hidden"
                    />
                  }
                >
                  <CalendarDays />
                  {selectedDate
                    ? format(selectedDate, "PPP", { locale: es })
                    : "Seleccioná tu fecha de nacimiento"}
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start">
                  <Calendar
                    mode="single"
                    locale={es}
                    captionLayout="dropdown"
                    startMonth={subYears(new Date(), 120)}
                    endMonth={latestAllowedBirthDate}
                    selected={selectedDate}
                    disabled={{ after: latestAllowedBirthDate }}
                    onSelect={(date) => {
                      field.onChange(date ? format(date, "yyyy-MM-dd") : "");
                      field.onBlur();
                      setDatePickerOpen(false);
                    }}
                  />
                </PopoverContent>
              </Popover>
              <FieldDescription className="text-xs">
                * Debes ser mayor de 18 años
              </FieldDescription>
              <FieldError>{fieldState.error?.message}</FieldError>
            </Field>
          );
        }}
      />

      <Controller
        control={control}
        name="nacionalidad"
        rules={{ required: "La nacionalidad es obligatoria" }}
        render={({ field, fieldState }) => (
          <Field data-invalid={fieldState.invalid}>
            <FieldLabel htmlFor="nacionalidad">Nacionalidad</FieldLabel>
            <Select
              name={field.name}
              value={field.value}
              onValueChange={(value) => {
                field.onChange(value);
                field.onBlur();
              }}
            >
              <SelectTrigger
                id="nacionalidad"
                ref={field.ref}
                aria-invalid={fieldState.invalid}
                className="w-full"
              >
                <SelectValue placeholder="Seleccioná tu nacionalidad" />
              </SelectTrigger>
              <SelectContent>
                {nationalityOptions.map((nationality) => (
                  <SelectItem key={nationality} value={nationality}>
                    {nationality}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <FieldError>{fieldState.error?.message}</FieldError>
          </Field>
        )}
      />
    </FieldGroup>
  );
};
