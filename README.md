# Trabajo final integrador - UTN

## Integrantes

- Matias Luna
- Tahiel Noé Heinze
- Lautaro Marin

## Problema Explicado

En el sector hotelero, la gestión manual o desorganizada de las reservas suele generar problemas recurrentes como la superposición de fechas, la falta de visibilidad en tiempo real sobre la disponibilidad de habitaciones y dificultades para mantener un historial centralizado de clientes. Esto no solo sobrecarga al personal administrativo, sino que impacta negativamente en la experiencia del huésped.

## Solución Concreta

Proponemos el desarrollo de una aplicación web centralizada para la gestión integral de reservas hoteleras. El sistema automatiza el flujo de consulta, reserva y administración de habitaciones, permitiendo a los clientes gestionar su estadía de forma autónoma y brindando al personal administrativo un panel de control centralizado para supervisar la ocupación y el historial del establecimiento.

## MVP Definido y Acotado

El MVP se enfoca estrictamente en el ciclo de vida esencial de una reserva y la gestión operativa básica del hotel:

- Gestión de Disponibilidad: Consulta de habitaciones según fechas y capacidad de huéspedes.
- Ciclo de Reserva: Creación, consulta de datos/estado, reprogramación de fechas y cancelación por parte del cliente.
- Panel de Administración: Visualización de reservas activas/futuras, estado de habitaciones por período y consulta de clientes.

## Funcionalidades Posteriores

Funcionalidades planeadas para etapas o versiones futuras post-entrega:

- Sistema de gestión de promociones, códigos de descuento y tarifas dinámicas por temporada.
- Facturación automática y generación de comprobantes.
- Gestión de servicios adicionales del hotel (room service, spa).
- Notificaciones automáticas por correo electrónico (confirmación de reserva, recordatorios de check-in).

## Fuera de Alcance

Para esta versión inicial MVP, quedan explícitamente excluidos:

- Procesamiento de pagos online: No se integrarán pasarelas de pago (Mercado Pago, etc.) por limitaciones de tiempo y alcance del proyecto, evitando además el manejo de datos financieros sensibles.
- Integración con plataformas externas: No habrá sincronización con otros sistemas de reserva externos (Airbnb, etc.).

## Roles y Permisos Detallados

#Cliente

Permisos:
- Consultar disponibilidad de habitaciones según fechas e integrantes.
- Crear reservas seleccionando habitaciones disponibles.
- Ver el detalle e historial de sus propias reservas.
- Reprogramar fechas de sus reservas (sujeto a disponibilidad).
- Cancelar sus propias reservas.

#Administrador

Permisos:
- Visualizar la totalidad de las reservas del hotel en curso, futuras y pasadas.
- Consultar el estado y detalle de cualquier reserva.
- Cancelar cualquier reserva en caso de ser necesario.
- Consultar el estado de ocupación de las habitaciones por períodos específicos.
- Acceder al historial completo de clientes y sus estadías previas.

## Stack Tecnológico

Frontend:
Framework: Next.js (React)
Estilos y Componentes: Tailwind CSS + shadcn/ui
Despliegue: Vercel

Backend:
Lenguaje y Framework: Python con FastAPI
Despliegue: Railway

Base de Datos:
Motor: PostgreSQL
Hosting: Neon (servidores en región SA/Brasil para menor latencia)

## Arquitectura y Estructura Prevista

Cliente / Web Front-end  --->  Next.js en Vercel
                                       │
                                   HTTP / REST
                                       ▼
API Back-end             --->  FastAPI en Railway
                                       │
                                  SQL Queries
                                       ▼
Base de Datos Relacional --->  PostgreSQL en Neon

Entidades Principales del Modelo de Datos
- Usuarios / Clientes: Datos personales y credenciales.
- Habitaciones: Tipo, capacidad, precio y estado.
- Reservas: Relación entre cliente, habitación, fechas de check-in/check-out y estado de la reserva.

## Repositorio

https://github.com/lautaromarin10/trabajo_final_integrador_UTN
