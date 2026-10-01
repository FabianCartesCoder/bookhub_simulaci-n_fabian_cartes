# 📖 BookHub - Aplicación Web de Gestión y Recomendación de Libros

Bienvenido a **BookHub**, una plataforma web interactiva desarrollada con **Flask** y **MySQL** siguiendo el patrón de arquitectura **MVC (Modelo-Vista-Controlador)**. La aplicación permite a los usuarios registrarse, iniciar sesión de forma segura, gestionar su propio catálogo de libros (CRUD) y marcar como favoritos los libros compartidos por la comunidad.

---

## 🚀 Características Principales

- **Autenticación y Seguridad:**
  - Registro e inicio de sesión de usuarios.
  - Encriptación de contraseñas utilizando **Bcrypt**.
  - Manejo de sesiones activas y protección de rutas privadas.
- **Gestión de Libros (CRUD):**
  - **Crear:** Publicar nuevos libros con título, autor, género, fecha de publicación y descripción.
  - **Leer:** Visualizar mis libros, explorar libros de la comunidad y ver detalles completos de cada obra.
  - **Editar:** Modificar información de los libros propios (campos pre-poblados).
  - **Eliminar:** Borrar registros propios con confirmación previa.
- **Interactividad y Favoritos:**
  - Agregar libros de otros usuarios a la lista personal de favoritos.
  - Visualizar la cantidad y los usuarios que han guardado cada libro como favorito.
- **Validaciones en Backend:**
  - Validación de campos requeridos, longitud de texto, formato de email y restricciones de fechas futuras.
  - Retroalimentación en tiempo real con mensajes `flash`.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Framework Web:** Flask
- **Base de Datos:** MySQL
- **Driver BD:** PyMySQL
- **Seguridad:** Flask-Bcrypt
- **Frontend:** HTML5, Jinja2, CSS3, Bootstrap 5, JavaScript (Vanilla)
- **Control de Versiones:** Git & GitHub

---

## 📁 Estructura del Proyecto (MVC)

```text
bookhub/
│
├── app/
│   ├── __init__.py            # Inicialización de Flask y Bcrypt
│   ├── config/
│   │   ├── __init__.py
│   │   └── mysqlconnection.py # Clase de conexión a la BD MySQL
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── users.py           # Rutas y lógica de usuarios (Auth)
│   │   └── books.py           # Rutas y lógica del CRUD de Libros
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # Consultas SQL y validaciones de usuarios
│   │   └── book.py            # Consultas SQL y validaciones de libros
│   ├── templates/
│   │   ├── base.html          # Plantilla base (Layout con Bootstrap)
│   │   ├── users/
│   │   │   └── index.html     # Registro e Inicio de Sesión
│   │   └── books/
│   │       ├── dashboard.html # Panel principal (Mis Libros / Comunidad)
│   │       ├── new.html       # Crear libro
│   │       ├── edit.html      # Editar libro
│   │       ├── show.html      # Detalle del libro y lista de favoritos
│   │       └── favorites.html # Mis libros favoritos
│   └── static/
│       ├── css/
│       │   └── style.css      # Estilos personalizados
│       └── js/
│           └── main.js        # Script cliente (confirmaciones)
│
├── resources/
│   ├── schema.sql             # Script de creación de la Base de Datos
│   └── erd.md                 # Diagrama Entidad-Relación (Mermaid)
│
├── .gitignore
├── README.md
├── requirements.txt
└── server.py                  # Archivo principal de ejecución