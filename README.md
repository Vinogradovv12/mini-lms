LMS Platform

Learning Management System built with FastAPI and designed with service-oriented architecture and role-based access control.

⸻

Features

Authentication & Authorization

* JWT authentication
* Login / Registration
* Role-Based Access Control (RBAC)
* Protected pages and API endpoints

⸻

Course Management

* Create courses
* Edit courses
* Delete courses
* Enroll into courses
* Course ownership validation

⸻

Lesson Management

* Create lessons
* View lessons
* Access validation

⸻

Administration

* Admin dashboard
* User overview
* Course statistics

⸻

Security

* Password hashing
* Custom domain exceptions
* Validation handlers
* Rate limiting
* Structured logging
* Separation of service and HTTP layers

⸻

Architecture

Project structure:

mini-lms/
├── alembic/
│   └── versions/
└── app/
    ├── authorization/
    ├── core/
    ├── dependencies/
    │   ├── api/
    │   └── frontend/
    ├── exceptions/
    ├── models/
    ├── routers/
    │   ├── api/
    │   └── frontend/
    ├── schemas/
    ├── services/
    ├── templates/
    │   └── errors/
    └── validation/

⸻

Technologies

* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Jinja2
* JWT
* Bootstrap

⸻

Run

Install dependencies:

pip install -r requirements.txt

Run server from /mini-lms:

python3 -m app.main

Open:

http://localhost:9090

⸻

Security Improvements

Implemented:

* Service Layer
* Domain Exceptions
* Response Schemas
* Validation
* RBAC
* Logging
* Error Pages

⸻

Future Improvements

* Docker
* Admin CRUD
* Course Analytics
* API Documentation
* CI/CD

⸻

Author

University practice project.