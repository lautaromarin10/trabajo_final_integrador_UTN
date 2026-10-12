import { Usuario_portal } from "@/types/usuario_portal";

export const getCurrentUser = async (): Promise<Usuario_portal> => {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/me`,
    { credentials: "include" },
  );

  if (!response.ok) {
    throw new Error(`No se pudo obtener el perfil: ${response.status}`);
  }

  return response.json();
};
