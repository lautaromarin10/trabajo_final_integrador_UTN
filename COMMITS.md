# Convención de Commits

En la etapa de desarrollo, todos los commits que se realicen deberán tener la siguiente estructura:

```bash
[BACK/FRONT/RAIZ]categoria(modulo): mensaje autoexplicativo
```

- Si un cambio afecta a más de un área, se pueden combinar las etiquetas con `&`,
  por ejemplo `[FRONT&RAIZ]`.
- Las etiquetas válidas son `BACK`, `FRONT` y `RAIZ`.
- El módulo y el mensaje deben describir el cambio realizado.

- Ejemplos prácticos

```bash
[FRONT]hotfix(reserva): mensaje 1
[BACK]feature(login): mensaje 2
[RAIZ]documentation(gitignore): mensaje 3
[FRONT&RAIZ]documentation(frontend): documenta la configuración del frontend
```

## Matriz de categorización

Lista de etiquetas a utilizar:

1. bug: Utilizada para fallos lógicos o en funcionalidades que rompen el comportamiento del sistema.
2. documentation: Utilizada para cambios o incorporación de documentación téncia para entender, usar o mantener el sistema
3. feature: Utilizada para la incorporación de nuevas funcionalidades o características al sistema.
4. refactor: Utilizada para modificaciones en el código destinado a mejorar su estructura, legibilidad o mantenibilidad sin modificar el comportamiento funcional.
5. chore: Utilizada para tareas de mantenimiento, configuración o actualizaciones que no incorporen nuevas funcionalidades ni corrigen funcionalidades.
6. core: Utilizada para identificar implementaciones o modificaciones relacionadas con funcionalidades centrales de la lógica de negocio, cuyo funcionamiento es vital para el sistema.
7. technical-debt: Utilizada para identificar código, decisiones técnicas o implementaciones que requieren una mejora para mantener la calidad, mantenibilidad o escalabilidad.
8. testing: Utilizada para cambios relacionados en incorporación, modificación o mantenimiento de pruebas automatizadas.
9. hotfix: Utilizada para correcciones urgentes de errores críticos que requieren una solución rapida.

## Validaciones de Git

Los hooks del repositorio ejecutan estas validaciones antes de crear cada commit:

- Cambios staged en `frontend/`: `pnpm lint` y `pnpm exec tsc --noEmit`.
- Cambios staged en `backend/`: `ruff check app` y compilación de los módulos Python.
- Mensaje del commit: verifica etiquetas, categoría, módulo y descripción según la convención anterior.

Para habilitarlos en cada clon del repositorio, ejecutar desde la raíz:

```bash
git config core.hooksPath .githooks
```
