"use client";

import { Button } from "@/components/ui/button";
import { logoutUser } from "@/services/auth/logout";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

const Logout = () => {
  const queryClient = useQueryClient();
  const router = useRouter();
  const { mutate, isPending, isError } = useMutation({
    mutationFn: logoutUser,
    onSuccess: () => {
      queryClient.clear();
      router.replace("/auth/signin");
      router.refresh();
    },
  });

  return (
    <div>
      <Button
        type="button"
        variant="outline"
        disabled={isPending}
        onClick={() => mutate()}
      >
        <LogOut />
        {isPending ? "Cerrando sesión..." : "Cerrar sesión"}
      </Button>
      {isError && (
        <p role="alert" className="absolute right-4 text-sm text-destructive">
          No se pudo cerrar la sesión. Intentá nuevamente.
        </p>
      )}
    </div>
  );
};

export default Logout;
