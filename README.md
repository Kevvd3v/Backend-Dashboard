# Backend-Dashboard
Backend desarrollado con FastAPI, PostgreSQL, SQLModel y Docker, encargado de almacenar, procesar y exponer datos del World Happiness Report.
Incluye autenticación JWT, carga de datos desde CSV, endpoints de consulta y un entorno completamente dockerizado para facilitar su despliegue.

## Tecnologías utilizadas
Python 3.11

FastAPI

SQLModel / SQLAlchemy

PostgreSQL 15

Docker & Docker Compose

JWT Authentication

Uvicorn

## Cómo levantar el proyecto con Docker
Asegúrate de tener Docker Desktop instalado.
1. Construir y levantar los contenedores
```
docker-compose up --build

```
## Colaboradores
Este repositorio está preparado para trabajo colaborativo.
Cada desarrollador sólo necesita:
```
git clone https://github.com/Kevd3v/Backend-Dashboard.git
cp .env.example .env
docker-compose up --build

```

