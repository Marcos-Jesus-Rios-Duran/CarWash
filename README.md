# 🧼 CarWash System - Backend

Este proyecto es una práctica de clase para un sistema de gestión de autolavado, desarrollado en **Python**. La arquitectura sigue un enfoque **Feature-First** combinado con patrones **MVC/DAO** para garantizar escalabilidad, seguridad y una clara separación de responsabilidades.

## 🚧🏗️🏢 Project Structure

La estructura del proyecto está organizada para ser modular y seguir los estándares internacionales de desarrollo:

```txt
/carwash_backend
├── /common
│   ├── /config
│   │   └── database.py          # Database connection
│   ├── /database
│   │   └── initialization.py    # Scripts to create tables and seeds
│   ├── /utils
│   │   ├── error_handlers.py    # Standardized API error responses
│   │   ├── route_names.py       # Constants for internal navigation
│   │   └── validators.py        # Input validation
│   └── /security
│       └── sanitizer.py         # SQL injection
├── /features
│   ├── /auth                    # Login, Register & Token management
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── /role
│   │   ├── dao.py               # CRUD for roles
│   │   ├── models.py            # Role table definition
│   │   └── schemas.py
│   ├── /user                    # Internal staff & admin management
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── /customer                # Client profiles & contact info
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── /vehicle                 # Car details (Plate, Color, Model)
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── /service                 # Catalog (Basic wash, Waxing, etc.)
│   │   ├── dao.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── schemas.py
│   └── /appointment             # Service-Vehicle
│       ├── dao.py
│       ├── models.py
│       ├── routes.py
│       └── schemas.py
├── .env                         # Environment variables
├── main.py                      # FastAPI/Flask entry point
└── requirements.txt             # Project dependencies
```
##

## 🛠️ Librerías Implementadas

### **Backend**

| Tecnología | Badge | Descripción | Documentación |
| :--- | :--- | :--- | :--- |
| **Python** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | Lenguaje base del proyecto. | [docs.python.org](https://docs.python.org/3/) |
| **FastAPI** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) | Framework para la creación de la API de alto rendimiento. | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **SQLAlchemy** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) | ORM para la gestión y comunicación con la base de datos. | [sqlalchemy.org](https://www.sqlalchemy.org/) |
| **Pydantic** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) | Validación de datos y gestión de Schemas. | [pydantic.dev](https://docs.pydantic.dev/) |
| **Uvicorn** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-202020?style=for-the-badge&logo=uvicorn&logoColor=white) | Servidor ASGI para la ejecución de la aplicación. | [uvicorn.org](https://www.uvicorn.org/) |
| **Dotenv** | ![Dotenv](https://img.shields.io/badge/Dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black) | Manejo de variables de entorno para seguridad. | [pypi.org](https://pypi.org/project/python-dotenv/) |


---
## 👨‍💻👨🏽Autor Creado por :
**Marcos Jesús Rios Duran** /[@Marcos-Jesús-Ríos-Durán](https://github.com/Marcos-Jesus-Rios-Duran)
Unidad 1
Seguridad en el Desarrollo de Aplicaciones
febrero 2024
