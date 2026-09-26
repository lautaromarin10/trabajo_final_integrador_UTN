# Convención de Commits

En la etapa de desarrollo, todos los commits que se realicen deberán tener la siguiente estructura:

```bash
[BACK/FRONT/RAIZ]categoria(modulo): mensaje autoexplicativo
```

- Ejemplos prácticos

```bash
[FRONT]hotfix(reserva): mensaje 1
[BACK]feature(login): mensaje 2
[RAIZ]documentation(gitignore): mensaje 3
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
