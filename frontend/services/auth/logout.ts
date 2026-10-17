export const logoutUser = async (): Promise<void> => {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/logout`,
    {
      method: "POST",
      credentials: "include",
    },
  );

  if (!response.ok) {
    throw new Error(`No se pudo cerrar la sesión: ${response.status}`);
  }
};
