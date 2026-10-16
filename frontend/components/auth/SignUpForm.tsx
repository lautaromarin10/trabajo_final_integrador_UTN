"use client";
import useSignUpForm from "@/hooks/auth/useSignUpForm";
import { FirstStepFields } from "./signUp/FirstStepFields";
import { SecondStepFields } from "./signUp/SecondStepFields";
import { Button } from "../ui/button";
import { Alert, AlertDescription } from "../ui/alert";
import { CircleCheck, InfoIcon } from "lucide-react";
import Link from "next/link";

const SignUpForm = () => {
  const {
    register,
    control,
    handleViewPassword,
    formState,
    viewPassword,
    getValues,
    handleSubmit,
    onSubmit,
    handleNextStep,
    handlePreviousStep,
    currentStep,
    hasNextStep,
    isLoading,
    isSuccess,
    signUpError,
  } = useSignUpForm();

  return (
    <>
      {isSuccess ? (
        <Alert className="bg-success/25 ">
          <CircleCheck className="text-success" />
          <AlertDescription className="text-black!">
            <div>Cuenta creada correctamente. </div>
            <Link href="/auth/signin" className="font-medium underline">
              Iniciá sesión
            </Link>
            .
          </AlertDescription>
        </Alert>
      ) : (
        <form className="w-full" onSubmit={handleSubmit(onSubmit)} noValidate>
          {signUpError && (
            <Alert variant="destructive" className="mb-4">
              <InfoIcon />
              <AlertDescription>{signUpError}</AlertDescription>
            </Alert>
          )}
          {currentStep === 1 ? (
            <FirstStepFields
              register={register}
              control={control}
              formState={formState}
            />
          ) : (
            <SecondStepFields
              register={register}
              getValues={getValues}
              formState={formState}
              handleViewPassword={handleViewPassword}
              viewPassword={viewPassword}
            />
          )}
          <div className="mt-4 flex gap-3">
            {!hasNextStep && (
              <Button
                type="button"
                variant="outline"
                className="flex-1"
                onClick={handlePreviousStep}
                disabled={isLoading}
              >
                Volver
              </Button>
            )}
            {hasNextStep ? (
              <Button type="button" className="w-full" onClick={handleNextStep}>
                Avanzar
              </Button>
            ) : (
              <Button type="submit" className="flex-1" disabled={isLoading}>
                {isLoading ? "Creando cuenta..." : "Crear cuenta"}
              </Button>
            )}
          </div>
        </form>
      )}
    </>
  );
};

export default SignUpForm;
