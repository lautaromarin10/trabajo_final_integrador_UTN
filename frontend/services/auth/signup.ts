import type { SignUpField } from "@/hooks/auth/useSignUpForm";

export const registerUser = async (data: SignUpField): Promise<void> => {
  const { password_validate, ...payload } = data;
  void password_validate;
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/register`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    const errorBody: unknown = await response.json().catch(() => null);
    let detail =
      "No se pudo crear la cuenta. Revisá los datos e intentá nuevamente.";
    if (
      typeof errorBody === "object" &&
      errorBody !== null &&
      "detail" in errorBody
    ) {
      if (typeof errorBody.detail === "string") {
        detail = errorBody.detail;
      } else if (Array.isArray(errorBody.detail)) {
        const messages = errorBody.detail.flatMap((issue) =>
          typeof issue === "object" &&
          issue !== null &&
          "msg" in issue &&
          typeof issue.msg === "string"
            ? [issue.msg]
            : [],
        );
        if (messages.length) detail = messages.join(". ");
      }
    }
    throw new Error(detail);
  }
};
