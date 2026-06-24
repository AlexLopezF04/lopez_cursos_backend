 # Proyecto de Cursos Online — Backend API REST

Backend de una plataforma de cursos online construido con **Django 6**, **Django REST Framework** y **PostgreSQL**. Incluye autenticación JWT, CRUD completo para 7 entidades, filtros, paginación y despliegue en Azure.

---

## Tecnologías

| Herramienta | Versión |
|---|---|
| Python | 3.13 |
| Django | 6.0.5 |
| Django REST Framework | 3.17.1 |
| djangorestframework-simplejwt | 5.5.1 |
| PostgreSQL | 15+ |
| Gunicorn | 26.0.0 |
| drf-nested-routers | 0.95.0 |

---

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd lopez_cursos
```

### 2. Crear y activar el entorno virtual

```bash
# Con uv (recomendado)
uv venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
uv pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y rellena tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus datos:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=lopez_cursos
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=True
```

### 5. Crear la base de datos en PostgreSQL

```sql
CREATE DATABASE lopez_cursos;
```

### 6. Aplicar migraciones

```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 8. Levantar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000`

---

## URL de despliegue

| Entorno | URL |
|---|---|
| Producción (Azure) | `http://158.23.59.71:8000` |
| Local | `http://127.0.0.1:8000` |

---

## Autenticación

La API usa **JWT (JSON Web Tokens)**. Para acceder a los endpoints protegidos debes:

### 1. Registrarse

```http
POST /api/auth/registro/
Content-Type: application/json

{
  "username": "alexander",
  "email": "alexander@email.com",
  "password": "password123",
  "rol": "estudiante"
}
```

### 2. Obtener token

```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "alexander",
  "password": "password123"
}
```

Respuesta:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

### 3. Usar el token en cada petición

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGci...
```

### 4. Refrescar token

```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

### 5. Cerrar sesión

```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

---

## Listado de endpoints

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/registro/` | Registrar nuevo usuario | No |
| POST | `/api/auth/login/` | Obtener token JWT | No |
| POST | `/api/auth/refresh/` | Refrescar token | No |
| POST | `/api/auth/logout/` | Invalidar token | Sí |

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/usuarios/` | Listar usuarios | Admin |
| GET | `/api/usuarios/{id}/` | Detalle de usuario | Sí |
| PATCH | `/api/usuarios/{id}/` | Actualizar usuario | Propietario/Admin |
| DELETE | `/api/usuarios/{id}/` | Eliminar usuario | Propietario/Admin |
| GET | `/api/usuarios/me/` | Perfil del usuario autenticado | Sí |
| PATCH | `/api/usuarios/me/` | Actualizar perfil propio | Sí |

### Categorías

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/categorias/` | Listar categorías | No |
| GET | `/api/categorias/{id}/` | Detalle de categoría | No |
| POST | `/api/categorias/` | Crear categoría | Admin |
| PUT/PATCH | `/api/categorias/{id}/` | Actualizar categoría | Admin |
| DELETE | `/api/categorias/{id}/` | Eliminar categoría | Admin |

### Cursos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/cursos/` | Listar cursos | No |
| GET | `/api/cursos/{id}/` | Detalle de curso | No |
| POST | `/api/cursos/` | Crear curso | Instructor/Admin |
| PUT/PATCH | `/api/cursos/{id}/` | Actualizar curso | Propietario/Admin |
| DELETE | `/api/cursos/{id}/` | Eliminar curso | Propietario/Admin |

**Filtros disponibles:**

```
GET /api/cursos/?nivel=basico
GET /api/cursos/?publicado=true
GET /api/cursos/?categoria=1
GET /api/cursos/?precio_min=10&precio_max=50
GET /api/cursos/?search=python
GET /api/cursos/?ordering=-precio
```

### Lecciones (anidadas en cursos)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/cursos/{curso_id}/lecciones/` | Listar lecciones | No |
| GET | `/api/cursos/{curso_id}/lecciones/{id}/` | Detalle de lección | No |
| POST | `/api/cursos/{curso_id}/lecciones/` | Crear lección | Instructor/Admin |
| PUT/PATCH | `/api/cursos/{curso_id}/lecciones/{id}/` | Actualizar lección | Instructor/Admin |
| DELETE | `/api/cursos/{curso_id}/lecciones/{id}/` | Eliminar lección | Instructor/Admin |

### Matrículas

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/matriculas/` | Listar matrículas propias | Sí |
| GET | `/api/matriculas/{id}/` | Detalle de matrícula | Sí |
| POST | `/api/matriculas/` | Matricularse en un curso | Sí |
| PATCH | `/api/matriculas/{id}/` | Actualizar estado | Sí |
| DELETE | `/api/matriculas/{id}/` | Cancelar matrícula | Admin |

**Filtros disponibles:**

```
GET /api/matriculas/?estado=activa
GET /api/matriculas/?curso=3
GET /api/matriculas/?fecha_desde=2025-01-01&fecha_hasta=2025-12-31
```

### Progreso

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/progresos/` | Listar progreso propio | Sí |
| GET | `/api/progresos/{id}/` | Detalle de progreso | Sí |
| POST | `/api/progresos/` | Registrar progreso | Sí |
| PATCH | `/api/progresos/{id}/` | Marcar lección completada | Sí |

### Reseñas (anidadas en cursos)

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/cursos/{curso_id}/resenas/` | Listar reseñas | No |
| GET | `/api/cursos/{curso_id}/resenas/{id}/` | Detalle de reseña | No |
| POST | `/api/cursos/{curso_id}/resenas/` | Crear reseña | Sí |
| PATCH | `/api/cursos/{curso_id}/resenas/{id}/` | Actualizar reseña | Propietario/Admin |
| DELETE | `/api/cursos/{curso_id}/resenas/{id}/` | Eliminar reseña | Propietario/Admin |

**Filtros disponibles:**

```
GET /api/cursos/{id}/resenas/?calificacion_min=4
GET /api/cursos/{id}/resenas/?calificacion_max=5
```

---

## Roles y permisos

| Rol | Descripción |
|-----|-------------|
| `estudiante` | Puede ver cursos, matricularse, registrar progreso y dejar reseñas |
| `instructor` | Puede crear y gestionar sus propios cursos y lecciones |
| `admin` | Acceso completo a todos los recursos |

---

## Paginación

Todos los listados usan paginación estándar con 10 resultados por página.

```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/cursos/?page=2",
  "previous": null,
  "results": []
}
```

---

## Ejemplos de uso con token

### Crear un curso (como instructor)

```http
POST /api/cursos/
Authorization: Bearer <token>
Content-Type: application/json

{
  "titulo": "Django REST Framework desde cero",
  "descripcion": "Aprende a construir APIs con Django",
  "precio": 29.99,
  "nivel": "basico",
  "categoria_id": 1,
  "publicado": true
}
```

### Matricularse en un curso

```http
POST /api/matriculas/
Authorization: Bearer <token>
Content-Type: application/json

{
  "curso": 1,
  "monto_pagado": 29.99
}
```

### Marcar una lección como completada

```http
PATCH /api/progresos/1/
Authorization: Bearer <token>
Content-Type: application/json

{
  "completada": true
}
```

### Dejar una reseña

```http
POST /api/cursos/1/resenas/
Authorization: Bearer <token>
Content-Type: application/json

{
  "calificacion": 5,
  "comentario": "Excelente curso, muy bien explicado."
}
```

---

### Descripción de las tablas

#### `store_usuario`
Extiende el modelo de usuario de Django (`AbstractUser`). Es la tabla central del sistema.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `username` | VARCHAR(150) | Nombre de usuario único |
| `email` | VARCHAR(254) | Correo electrónico |
| `password` | VARCHAR(128) | Contraseña hasheada |
| `first_name` | VARCHAR(150) | Nombre |
| `last_name` | VARCHAR(150) | Apellido |
| `rol` | VARCHAR(20) | `estudiante` / `instructor` / `admin` |
| `bio` | TEXT | Descripción del perfil |
| `foto` | VARCHAR | Ruta de la imagen de perfil |
| `is_active` | BOOLEAN | Cuenta activa |
| `is_staff` | BOOLEAN | Acceso al admin de Django |
| `created_at` | TIMESTAMPTZ | Fecha de registro |
| `updated_at` | TIMESTAMPTZ | Última actualización |

#### `store_categoria`
Clasifica los cursos por tema.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `nombre` | VARCHAR(100) | Nombre de la categoría (único) |
| `slug` | VARCHAR(50) | Versión URL del nombre (único) |

#### `store_curso`
Contiene la información principal de cada curso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `instructor_id` | FK → store_usuario | Instructor que creó el curso |
| `categoria_id` | FK → store_categoria | Categoría del curso |
| `titulo` | VARCHAR(200) | Título del curso |
| `descripcion` | TEXT | Descripción completa |
| `precio` | DECIMAL(8,2) | Precio en dólares |
| `nivel` | VARCHAR(20) | `basico` / `intermedio` / `avanzado` |
| `publicado` | BOOLEAN | Visible para estudiantes |
| `created_at` | TIMESTAMPTZ | Fecha de creación |
| `updated_at` | TIMESTAMPTZ | Última actualización |

#### `store_leccion`
Unidades de contenido dentro de un curso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `curso_id` | FK → store_curso | Curso al que pertenece |
| `titulo` | VARCHAR(200) | Título de la lección |
| `contenido` | TEXT | Texto de la lección |
| `video_url` | VARCHAR | URL del video |
| `orden` | INT | Posición dentro del curso |
| `duracion_min` | INT | Duración estimada en minutos |

#### `store_matricula`
Registro de inscripción de un estudiante a un curso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `usuario_id` | FK → store_usuario | Estudiante inscrito |
| `curso_id` | FK → store_curso | Curso en el que se inscribió |
| `fecha_pago` | TIMESTAMPTZ | Fecha y hora de la inscripción |
| `monto_pagado` | DECIMAL(8,2) | Monto abonado |
| `estado` | VARCHAR(20) | `activa` / `vencida` / `cancelada` |

> **Restricción:** un usuario no puede matricularse dos veces en el mismo curso.

#### `store_progreso`
Registra el avance de un estudiante lección por lección.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `matricula_id` | FK → store_matricula | Matrícula asociada |
| `leccion_id` | FK → store_leccion | Lección evaluada |
| `completada` | BOOLEAN | Si la lección fue completada |
| `fecha_completado` | TIMESTAMPTZ | Cuándo se completó |

> **Restricción:** una matrícula no puede registrar progreso duplicado para la misma lección.

#### `store_resena`
Opinión y calificación de un estudiante sobre un curso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | BigInt (PK) | Identificador único |
| `usuario_id` | FK → store_usuario | Estudiante que escribe la reseña |
| `curso_id` | FK → store_curso | Curso calificado |
| `calificacion` | SMALLINT | Valor del 1 al 5 |
| `comentario` | TEXT | Texto libre (opcional) |
| `created_at` | TIMESTAMPTZ | Fecha de la reseña |

> **Restricción:** un usuario solo puede dejar una reseña por curso.

---

## Arquitectura del proyecto

```
lopez_cursos/                        <- Raiz del proyecto
|
+-- config/                          <- Configuracion global de Django
|   +-- settings.py                  <- Apps, JWT, CORS, base de datos
|   +-- urls.py                      <- Enrutador principal (auth + API)
|   +-- wsgi.py                      <- Entrada para servidores WSGI (Gunicorn)
|   +-- asgi.py                      <- Entrada para servidores ASGI
|
+-- store/                           <- Aplicacion principal del negocio
|   |
|   +-- models/                      <- Capa de datos (ORM de Django)
|   |   +-- __init__.py              <- Exporta todos los modelos
|   |   +-- usuario.py               <- Modelo Usuario (extiende AbstractUser)
|   |   +-- categoria.py             <- Modelo Categoria
|   |   +-- curso.py                 <- Modelo Curso
|   |   +-- leccion.py               <- Modelo Leccion
|   |   +-- matricula.py             <- Modelo Matricula
|   |   +-- progreso.py              <- Modelo Progreso
|   |   +-- resena.py                <- Modelo Resena
|   |
|   +-- serializers/                 <- Transformacion y validacion de datos
|   |   +-- __init__.py              <- Exporta todos los serializers
|   |   +-- usuario.py               <- UsuarioSerializer, UsuarioCreateSerializer
|   |   +-- categoria.py             <- CategoriaSerializer
|   |   +-- curso.py                 <- CursoSerializer, CursoListSerializer
|   |   +-- leccion.py               <- LeccionSerializer
|   |   +-- matricula.py             <- MatriculaSerializer (valida duplicados)
|   |   +-- progreso.py              <- ProgresoSerializer (auto fecha_completado)
|   |   +-- resena.py                <- ResenaSerializer (valida duplicados)
|   |
|   +-- views/                       <- Logica de negocio y endpoints
|   |   +-- __init__.py              <- Exporta todos los ViewSets
|   |   +-- usuario.py               <- UsuarioViewSet + RegistroView
|   |   +-- categoria.py             <- CategoriaViewSet
|   |   +-- curso.py                 <- CursoViewSet (filtros, busqueda, permisos)
|   |   +-- leccion.py               <- LeccionViewSet (rutas anidadas)
|   |   +-- matricula.py             <- MatriculaViewSet
|   |   +-- progreso.py              <- ProgresoViewSet
|   |   +-- resena.py                <- ResenaViewSet (rutas anidadas)
|   |
|   +-- migrations/                  <- Historial de cambios en la base de datos
|   |   +-- 0001_initial.py          <- Creacion inicial de todas las tablas
|   |   +-- 0002_alter_*.py          <- Ajustes posteriores
|   |
|   +-- tests/                       <- Pruebas automatizadas por entidad
|   |   +-- test_usuario.py
|   |   +-- test_categoria.py
|   |   +-- test_curso.py
|   |   +-- test_matricula.py
|   |   +-- test_resena.py
|   |
|   +-- filters.py                   <- Filtros por precio, estado, fecha, calificacion
|   +-- permissions.py               <- Permisos por rol (Instructor, Admin, Propietario)
|   +-- pagination.py                <- Paginacion estandar (10 resultados/pagina)
|   +-- admin.py                     <- Modelos registrados en Django Admin
|   +-- urls.py                      <- Rutas con routers anidados
|
+-- cursos/                          <- Aplicacion auxiliar
|   +-- health.py                    <- Endpoint GET /api/health/
|
+-- .env                             <- Variables de entorno locales (no se sube a Git)
+-- .env.example                     <- Plantilla de variables de entorno
+-- .gitignore                       <- Archivos excluidos de Git
+-- .python-version                  <- Version de Python del proyecto (3.13)
+-- manage.py                        <- Comando principal de Django
+-- pyproject.toml                   <- Dependencias declaradas con uv
+-- requirements.txt                 <- Dependencias exportadas para despliegue
+-- uv.lock                          <- Versiones exactas bloqueadas por uv
+-- README.md                        <- Este archivo
```

### Descripción de cada capa

**`config/`** — Cerebro de la configuración. El archivo `settings.py` centraliza todo: conexión a PostgreSQL, apps instaladas, configuración de JWT (tiempo de vida del token, rotación automática), CORS para el frontend y la clase de paginación por defecto.

**`store/models/`** — Define la estructura de la base de datos. Cada archivo representa una tabla. Se usan relaciones `ForeignKey` para conectar entidades. Por ejemplo, un `Curso` pertenece a un `Usuario` instructor y a una `Categoria`, y una `Matricula` conecta a un `Usuario` con un `Curso`.

**`store/serializers/`** — Convierte objetos de la base de datos a JSON y viceversa. También aplica validaciones de negocio, como verificar que un usuario no se matricule dos veces en el mismo curso, o que la fecha de completado se registre automáticamente al marcar una lección.

**`store/views/`** — Contiene los `ViewSet` que procesan cada petición HTTP. Aquí se definen los permisos por acción (quién puede crear, editar o borrar), los filtros aplicables y la lógica específica de cada endpoint.

**`store/filters.py`** — Define filtros avanzados con `django-filter`. Permite a los clientes filtrar resultados usando parámetros en la URL como `?precio_min=10&precio_max=50`, `?estado=activa` o `?calificacion_min=4`.

**`store/permissions.py`** — Centraliza las reglas de acceso con cuatro clases reutilizables: `EsSoloLectura`, `EsInstructor`, `EsPropietarioOAdmin` y `EsAdminDjango`. Estas se combinan en las vistas según la acción que se ejecuta.

**`store/urls.py`** — Usa `drf-nested-routers` para generar rutas anidadas automáticamente, habilitando URLs como `/api/cursos/1/lecciones/` y `/api/cursos/1/resenas/` sin escribir cada ruta manualmente.
