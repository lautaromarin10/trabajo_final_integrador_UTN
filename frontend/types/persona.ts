export interface Persona {
  id: number;
  created_at: string;
  updated_at: string;
  deleted: boolean;
  deleted_at: string | null;
  nombre: string;
  apellido: string;
  tipo_documento: string;
  numero_documento: string;
  fecha_nacimiento: string;
  nacionalidad: string;
  observaciones: string | null;
}
