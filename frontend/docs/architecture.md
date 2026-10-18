# Cómo organizamos las carpetas

Organizamos el código por responsabilidad: lo que se comparte va en carpetas comunes y lo específico de una funcionalidad tiene que quedar cerca de ella.

## `components/`

- `globals/`: componentes que aparecen en distintas partes de la app, como el
  `Header`, la navegación o el `Logo`.
- `ui/`: componentes visuales reutilizables, como los de shadcn/ui (`Button`,
  `Input`, `Select`, etc.). Van las piezas genéricas, no componentes con
  lógica de un dominio.
- `[dominio]/`: componentes propios de una funcionalidad. Por ejemplo, los
  formularios de login y signup van en `auth/`.

## `hooks/` y `services/`

Ordenarlos por dominio cuando estén ligados a una funcionalidad: por ejemplo,
`hooks/auth/` o `services/auth/`. Si algo es realmente compartido y no pertenece
a ningún dominio, puede ir en la raíz de su carpeta.

## `types/`

Acá van los tipos del dominio, como `Persona` o `UsuarioPortal`. Las props y los
tipos que usa un solo componente dejarlos en el mismo archivo del componente. Si
los necesitan varios componentes, ahí sí tiene sentido compartirlos.

## `utils/`

Si una utilidad es de un dominio, guardarla ahí; por ejemplo,
`utils/auth/regex.ts`. Si sirve en distintas partes y no es de un dominio en
particular, puede ir directamente en `utils/`. No hace falta crear un helper
compartido para algo que se usa una sola vez.
