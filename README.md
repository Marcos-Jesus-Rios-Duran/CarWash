# 🧼 CarWash System - Backend

This project is a class assignment for a a **Car Wash Backend**, developed in **Python**. The architecture follows a **Feature-First** approach combined whit **MVC/DAO** patterns to ensure scalability, security, and  clear separetions of responsabilities.

## 🚧🏗️🏢 Project Structure

The project structure is organizaded to be modular and follows international devolopment standards:

```txt
/carwash_backend
├── /common
│   ├── /config
|   |   ├──config.py
│   │   └── database.py          # Database connection
│   ├── /database
│   │   └── create_db.py         # Scripts to create tables and seeds
│   ├── /utils
│   │   ├── message_handlres.py  # Standardized message
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
## 👨‍💻Virtual Enviroment
To create the virtual enviroment: <br/>
**Windows:**

```bash
python -m venv venv
```
to activate the enviroment:
~~~ bash
venv\Scripts\activate
~~~



## 🛠️ Libraries

### **Backend**

| Tecnología | Badge | Descripción | Documentación |
| :--- | :--- | :--- | :--- |
| **Python** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) | Base lenguage of the project. | [docs.python.org](https://docs.python.org/3/) |
| **FastAPI** | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) | Framework for creating hig-performance Apis. | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **SQLAlchemy** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white) | ORM for databases management and communication. | [sqlalchemy.org](https://www.sqlalchemy.org/) |
| **Pydantic** | ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white) | Data validation and Schema management | [pydantic.dev](https://docs.pydantic.dev/) |
| **Uvicorn** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-202020?style=for-the-badge&logo=uvicorn&logoColor=white) |ASGI server to run the application. | [uvicorn.org](https://www.uvicorn.org/) |
| **Dotenv** | ![Dotenv](https://img.shields.io/badge/Dotenv-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black) | Environment variable management for security. | [pypi.org](https://pypi.org/project/python-dotenv/) |


---
## 👨‍💻👨🏽Author
Created by:
**Marcos Jesús Rios Duran** /[@Marcos-Jesús-Ríos-Durán](https://github.com/Marcos-Jesus-Rios-Duran)
unit 1
Application Development Security
february 2026
