import { Persona } from "@/types/persona";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { type SubmitHandler, useForm } from "react-hook-form";
import { registerUser } from "@/services/auth/signup";

interface Portal_User_Field {
  email: string;
  password: string;
  password_validate: string;
}

export type SignUpField = Portal_User_Field &
  Pick<
    Persona,
    | "nombre"
    | "apellido"
    | "fecha_nacimiento"
    | "numero_documento"
    | "tipo_documento"
    | "nacionalidad"
  >;

export type viewPasswordField = "password" | "password_validate";

const NUMBER_STEPS = 2;
const INITIAL_STEP = 1;

const useSignUpForm = () => {
  const {
    register,
    control,
    formState,
    handleSubmit,
    trigger,
    getValues,
  } = useForm<SignUpField>({
    defaultValues: {
      nombre: "",
      apellido: "",
      fecha_nacimiento: "",
      tipo_documento: "",
      numero_documento: "",
      nacionalidad: "",
      email: "",
      password: "",
      password_validate: "",
    },
  });

  const [viewPassword, setViewPassword] = useState<
    Record<viewPasswordField, boolean>
  >({
    password: false,
    password_validate: false,
  });

  const handleViewPassword = (field: viewPasswordField) => {
    setViewPassword((prev) => ({
      ...prev,
      [field]: !prev[field],
    }));
  };

  const [currentStep, setCurrentStep] = useState(INITIAL_STEP);
  const hasNextStep = currentStep < NUMBER_STEPS;

  const { mutate, isLoading, isSuccess, error, reset } = useMutation({
    mutationFn: registerUser,
  });

  const handleNextStep = async () => {
    const isValid = await trigger([
      "nombre",
      "apellido",
      "tipo_documento",
      "numero_documento",
      "fecha_nacimiento",
      "nacionalidad",
    ]);
    if (isValid) setCurrentStep(2);
  };

  const handlePreviousStep = () => {
    reset();
    setCurrentStep(1);
  };

  const onSubmit: SubmitHandler<SignUpField> = (data) => {
    reset();
    mutate(data);
  };

  return {
    register,
    control,
    getValues,
    handleViewPassword,
    viewPassword,
    formState,
    handleSubmit,
    onSubmit,
    currentStep,
    hasNextStep,
    handleNextStep,
    handlePreviousStep,
    isLoading,
    isSuccess,
    signUpError: error instanceof Error ? error.message : "",
  };
};

export default useSignUpForm;
