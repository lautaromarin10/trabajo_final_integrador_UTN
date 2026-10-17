import { Persona } from "./persona";

export interface Usuario_portal {
  id: number;
  created_at: string;
  updated_at: string;
  deleted: boolean;
  deleted_at: string | null;
  persona_id: number | null;
  role: "admin" | "user";
  email: string;
  ultimo_ingreso: string | null;
  persona: Persona;
}
