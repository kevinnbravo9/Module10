# FastAPI Calculator – Module 10

## Project Description

This project extends my FastAPI Calculator application from Assignments 8 and 9 by adding database integration and secure user management components.

The application supports basic calculator operations through a web interface and FastAPI endpoints. Module 9 introduced PostgreSQL and database operations, while Module 10 focuses on SQLAlchemy models, Pydantic validation, password hashing, automated testing, and CI/CD deployment.

## GitHub Repository

https://github.com/kevinnbravo9/Module10

## Docker Hub

https://hub.docker.com/r/kevinbravor99/fastapi-calculator-module10

Docker image:

`kevinbravor99/fastapi-calculator-module10:latest`

## Technologies Used

- Python
- FastAPI and Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- Argon2 password hashing using pwdlib
- Pytest and pytest-cov
- Playwright
- Docker and Docker Compose
- GitHub Actions
- Trivy security scanning
- HTML

## Calculator Features

The application supports:

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero validation
- Calculator web interface
- FastAPI endpoints

## Module 9 – PostgreSQL Integration

Module 9 introduced PostgreSQL through Docker Compose, along with pgAdmin for database management.

I practiced creating database tables, inserting records, updating records, deleting records, and querying related data using SQL.

The database work included users and calculations, demonstrating relationships between tables.

## Module 10 – Secure User Management

Module 10 adds a SQLAlchemy `User` model containing:

- `id` – Unique user identifier
- `username` – Unique username
- `email` – Unique email address
- `password_hash` – Stored password hash
- `created_at` – User creation timestamp

### Pydantic Validation

The project includes two Pydantic schemas:

**UserCreate**

Validates incoming user information, including username, email address, and password.

**UserRead**

Represents user information returned by the application without exposing the stored password hash.

### Password Security

Passwords are hashed using Argon2 through the `pwdlib` library.

The project includes functions for hashing passwords and verifying entered passwords against stored hashes.

Plaintext passwords are not stored in the user records created by the Module 10 user service.

### Database Operations

SQLAlchemy is used to communicate with PostgreSQL.

The user service supports creating user records, storing password hashes, and handling duplicate username or email errors.

## Running the Application Locally

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

Open:

http://localhost:8000

API documentation:

http://localhost:8000/docs

## PostgreSQL with Docker Compose

Start the configured services:

```bash
docker compose up -d
```

This starts the application and PostgreSQL environment using the project's Docker Compose configuration.

The application database and the separate test database must be configured before running database integration tests.

## Automated Testing

The project includes unit, integration, and end-to-end tests.

Run unit tests:

```bash
python -m pytest tests/unit -v
```

Run integration tests:

```bash
python -m pytest tests/integration -v
```

Run end-to-end tests:

```bash
python -m pytest tests/e2e -v
```

Run unit and integration tests together:

```bash
python -m pytest tests/unit tests/integration -v
```

During local Module 10 verification, all 36 unit and integration
tests passed with 100% coverage of the application modules measured
by pytest-cov.

The GitHub Actions workflow successfully completed its test, security,
and deploy jobs. The Docker image was published to Docker Hub and
verified by pulling and running the published image. The FastAPI
documentation endpoint returned HTTP 200.

The security pipeline uses Trivy to scan the Docker image for
HIGH and CRITICAL vulnerabilities before deployment. 