# Trabajo final integrador - UTN

## Integrantes

- Matias Luna
- Tahiel Noé Heinze
- Lautaro Marin

## Propuesta del proyecto

Para nuestro Trabajo Final Integrador proponemos desarrollar una aplicación web orientada a la gestión de reservas para establecimientos hoteleros. El sistema permitirá centralizar y organizar la información relacionada con las reservas, habitaciones y clientes, facilitando tanto la experiencia del huésped como las tareas administrativas del establecimiento.

La aplicación tendrá dos perfiles principales: Cliente y Administrador. El cliente podrá consultar la disponibilidad, realizar y gestionar sus propias reservas según las fechas de estadía y la cantidad de huéspedes. Por otro lado, el administrador contará con un panel de gestión desde el cual podrá supervisar las reservas actuales y futuras, consultar el estado de las habitaciones y acceder al historial de clientes.

## Funcionalidades incluidas

### Cliente

- Consultar la disponibilidad de habitaciones según las fechas de ingreso, egreso y la cantidad de huéspedes.
- Crear una reserva seleccionando una habitación disponible.
- Consultar el estado y los datos de su reserva.
- Reprogramar una reserva, siempre que exista disponibilidad para las nuevas fechas
- Cancelar una reserva.

### Administrador

- Visualizar todas las reservas en curso y futuras.
- Consultar el detalle y estado de cada reserva.
- Cancelar reservas cuando sea necesario.
- Consultar la disponibilidad y el estado de las habitaciones.
- Identificar qué habitaciones se encuentran reservadas y durante qué período.
- Consultar el historial de clientes y sus reservas anteriores.

## Funcionalidades excluidas

En esta primera versión se excluye la implementación de un sistema de gestión y procesamiento de pagos. Esta funcionalidad queda fuera del alcance debido a las limitaciones de tiempo y recursos del proyecto, además de requerir consideraciones adicionales relacionadas con la seguridad y el tratamiento de información financiera.

También quedan fuera del alcance inicial otras funcionalidades complementarias, como la gestión de promociones y descuentos, facturación, integración con plataformas externas y servicios adicionales del establecimiento.

## Stack Tecnológico

En cuanto a las tecnologías utilizaremos lenguajes y frameworks modernos y reconocidos en la industria. Para el Frontend utilizaremos Next.js, acompañado de Tailwind CSS y shadcn/ui para el desarrollo de la interfaz. Esto nos permitirá construir una aplicación moderna, responsive y con componentes reutilizables

Para el Backend utilizaremos Python junto con FastAPI, lo que nos permitirá desarrollar una API REST rápida, escalable y organizada. Además, FastAPI nos facilitará la validación de datos y la implementación de la lógica de negocio necesaria para gestionar los turnos

Para la Base de Datos utilizaremos PostgreSQL, debido a que al tratarse de un sistema de turnos debemos tener entidades relacionadas, como usuarios, clientes, profesionales y turnos, lo que nos permitirá establecer relaciones claras entre los datos y garantizar la integridad y su consistencia.

En cuanto al despliegue del proyecto, proponemos utilizar Vercel para el Frontend, ya que al ser la plataforma desarrolladora de Next.js nos proporicona una integración muy sencilla con el framework, además de que facilita el despliegue mediante repositorios de GitHub

Para el Backend, consideramos utilizar Railway, ya que consideramos que se adapta a las necesidades del proyecto y a los recursos disponibles, además de su facilidad de configuración y despliegue.

Por último, para alojar nuestra Base de Datos pOstgreSQL utilizaremos Neon, ya que ofrece planes gratuitos adecuados a las necesidades del proyecto y cuenta con infraestructura en regiones cercanas a Argentina, como Brasil, lo que nos permitirá reducir la latencia en la conexión con la base de datos.

## Enlace al Repositorio

https://github.com/lautaromarin10/trabajo_final_integrador_UTN
