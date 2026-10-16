import { useState } from "react";
import { signInUser } from "@/services/auth/signin";
import { getCurrentUser } from "@/services/auth/getCurrentUser";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { SubmitHandler, useForm } from "react-hook-form";
import { useRouter } from "next/navigation";

interface signInFields {
  email: string;
  password: string;
}

const useSignInForm = () => {
  const queryClient = useQueryClient();
  const router = useRouter();
  const { register, formState, handleSubmit } = useForm<signInFields>({
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const [viewPassword, setViewPassword] = useState<boolean>(false);
  const [signInError, setSignInError] = useState<string>("");

  const handleViewPassword = () => {
    setViewPassword(!viewPassword);
  };

  const { mutate, error, data } = useMutation({
    mutationFn: async ({ email, password }: signInFields) => {
      await signInUser(email, password);
      return queryClient.fetchQuery({
        queryKey: ["auth", "me"],
        queryFn: getCurrentUser,
      });
    },
    onSuccess: (user) => {
      router.replace(user.role === "admin" ? "/admin" : "/user");
    },
    onError: () => {
      setSignInError(
        "No se pudo iniciar sesión. Verificá tus datos e intentá nuevamente.",
      );
    },
  });

  const onSubmit: SubmitHandler<signInFields> = (data) => {
    setSignInError("");
    if (data.email && data.password) {
      mutate({ email: data.email, password: data.password });
    }
  };

  return {
    viewPassword,
    handleViewPassword,
    error,
    data,
    register,
    formState,
    handleSubmit,
    onSubmit,
    signInError,
  };
};

export default useSignInForm;
