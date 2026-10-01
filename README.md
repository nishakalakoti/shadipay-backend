# ShadiPay Backend

A clean backend foundation for ShadiPay.

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic
- python-dotenv
- psycopg2-binary

## Setup on Windows

Create the virtual environment:

```powershell
py -3 -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Set the local PostgreSQL connection in `.env` using `DATABASE_URL`.

## Run the Server

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Documentation and Health Check

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
- Health check: http://127.0.0.1:8000/health

No business APIs or database tables have been added yet.
