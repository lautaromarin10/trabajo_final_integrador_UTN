//Sign in
export const signInUser = async (email: string, password: string) => {
  const ROUTE = `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/login`;

  try {
    const response = await fetch(ROUTE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (!response.ok) {
      throw new Error("Error, STATUS: " + response.status);
    }

    const data = await response.json();

    return data;
  } catch (error) {
    throw error;
  }
};
