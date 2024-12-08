
Optime API
==========

Arquitectura: Hexagonal + Vertical Slicing + Screaming
------------------------------------------------------

Optime API está diseñada utilizando los principios de arquitectura hexagonal, lo que significa que está organizada en capas desacopladas para facilitar su mantenimiento, escalabilidad y pruebas. Esta arquitectura también incorpora vertical slicing para estructurar el código en funciones por características y screaming architecture para asegurar que el dominio sea el aspecto más evidente del diseño.

1. Dominio (Domain)
-------------------

El dominio es el núcleo de la aplicación, donde se definen las reglas y la lógica de negocio. Es completamente independiente de las tecnologías subyacentes como bases de datos o servidores. Aquí se encuentran las entidades, interfaces de repositorios y excepciones del dominio.

**Archivos Clave:**
    - **Entidades:** Clases que representan los datos principales de la aplicación, como `Notification`, `Payment`, `User`.
      Ejemplo: `src/notifications/domain/Notification.py`
      
    - **Interfaces de Repositorio:** Definen cómo se accede y manipulan los datos en el almacenamiento sin preocuparse por su implementación.
      Ejemplo: `src/notifications/domain/NotificationRepository.py`
      
    - **Excepciones:** Manejan errores específicos del dominio para mantener la consistencia en las reglas de negocio.
      Ejemplo: `src/notifications/domain/exceptions.py`


2. Aplicación (Application)
---------------------------

Esta capa es responsable de coordinar los casos de uso de la lógica del dominio. Los casos de uso utilizan las entidades del dominio para ejecutar las operaciones necesarias y siguen siendo independientes de la infraestructura (bases de datos, APIs, etc.).

**Archivos Clave:**
    - **Casos de Uso:** Clases que implementan la lógica para manejar acciones específicas como crear o modificar notificaciones.
      Ejemplo: `src/notifications/application/NotificationCreator.py`
      
    - **Aplicación de Servicios:** Orquestación de operaciones que interactúan con varias entidades del dominio.
      Ejemplo: `src/notifications/application/NotificationSender.py`


3. Infraestructura (Infrastructure)
-----------------------------------

Esta capa contiene la implementación concreta de los detalles técnicos como la persistencia de datos (bases de datos), peticiones HTTP y la integración con servicios externos (Mercado Pago, APIs de mensajería, etc.).

**Archivos Clave:**
    - **Adaptadores de Repositorio:** Implementaciones de las interfaces de repositorio que conectan con la base de datos.
      Ejemplo: `src/notifications/infrastructure/MySqlNotificationRepository.py`
      
    - **Controladores HTTP:** Gestionan las peticiones y respuestas HTTP, exponiendo los endpoints de la API.
      Ejemplo: `src/notifications/infrastructure/NotificationRoutes.py`
      
    - **Conexión a Servicios Externos:** Implementaciones que permiten la interacción con APIs externas como Mercado Pago.
      Ejemplo: `src/payments/infrastructure/PaymentRoutes.py`
      
    - **Configuraciones de Base de Datos:** Configura la conexión y detalles de la base de datos.
      Ejemplo: `src/config/database.py`


Guía de Instalación y Ejecución
===============================

**Requerimientos:**
  - MySQL Server
  - Python 3.11
  - nodejs 
  - Ngrok
  - Channels

**Pasos para la Instalación:**
  1. Clonar el repositorio: `git clone <url-del-repositorio>`
  2. Crear un entorno virtual: `python -m venv venv`
  3. Activar el entorno virtual:
      - Windows: `venv\Scriptsctivate`
      - macOS/Linux: `source venv/bin/activate`
  4. Instalar las dependencias: `pip install -r requirements.txt` o `npm install ` dependiendo la tecnologia del microservicio. 
  5. Ejecutar el script `config/create_db_user.sql` en tu administrador de base de datos.
  6. Crear el archivo `.env` utilizando el ejemplo proporcionado en el proyecto .envExample.
  7. Configurar los tokens de acceso de servicios externos como Mercado Pago o Meta API en tu archivo `.env`.
  8. Ejecutar las migraciones de la base de datos: `alembic upgrade head`
  9. Iniciar ngrok para exponer tu aplicación: `ngrok http 8000`.
  10. Agregar el URL  de ngrok en el archivo `.env`.
  11. Iniciar la aplicación: `uvicorn main:app --reload`
  12. En caso de usar certificados ssl `uvicorn main:app --host 0.0.0.0 --port $PORT --reload --ssl-keyfile=$SSL_KEYFILE --ssl-certfile=$SSL_CERTFILE`
  13. En caso de usar microservicios `uvicorn main:app --reload --port *puerto a usar*`
  14. En caso de usar microservicios `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
  15. Para poder correr los channels debemos de instalar los siguientes paquetes: `npm install amqplib cors dotenv express mysql2`
  16. Para ejecutar los channels debemos de escribir los siguientes comandos: `npm run dev` o `nodemon server.js`

  
  12. Testear los endpoints utilizando Postman: [Documentación de Postman Api-Optime](https://documenter.getpostman.com/view/30415321/2sAXxLBZW6#79b970a8-df6b-486c-936c-eb714da4815cT)

**Ejecución de Pruebas:**
Para ejecutar los tests:
  1. Ejecutar `pytest` en el directorio raíz del proyecto para correr las pruebas unitarias.
  2. Integración con GitHub Actions para la ejecución automática de tests en cada push o pull request.

