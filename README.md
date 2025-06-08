# AssetsManagement
Centralized application for tracking and managing organizational assets with user authentication and tagging, built with a Flask + React + PostgreSQL stack and fully dockerized.

## Features
- User authentication & session management via JWT tokens and secure password handling

- Asset CRUD operations, including search, filtering, tagging, and categorization

- Project and tag management with relationships across multiple assets

- RESTful API implemented using Flask blueprints (/auth, /asset, /project, /tag, /type)

- Data validation through Pydantic schemas

- Persistent PostgreSQL backend, managed via schema and connection modules

- Modular and testable codebase, with full Test suite and code coverage tools

- Robust parameter/config management, protected routes, and standardized error responses

- Docker support, enabling easy local development and deployment

## Tech Stack

| Layer        | Technology                |
|--------------|----------------------------|
| **Backend**  | Python, Flask, Flask Blueprints |
| **Validation** | Pydantic models          |
| **Database** | PostgreSQL via Psycopg     |
| **Frontend** | React (JSX, REST calls)    |
| **Dev Tools**| Docker, Docker Compose     |
| **Testing**  | Pytest, Coverage           |


## Getting Started
Prerequisites:
    - Docker & Docker Compose installed

      (Alternatively) Python 3.10+, Node.js 16+, PostgreSQL 13+

### Quick Setup (Docker)
1. Clone the repo:

    git clone https://github.com/zainabj18/AssetsManagement.git

    cd AssetsManagement

2. Build and start containers:

    docker-compose up --build

3. Access services:

    - Backend API: http://localhost:5000/api/v1/

    - Frontend UI: http://localhost:3000/

### Manual Setup (Without Docker)
Backend

1. Enter backend folder:

    - cd backend

2. Create and activate virtual environment:

    - python3 -m venv venv && source venv/bin/activate

3. Install dependencies:

    - pip install -r requirements.txt
  
4. Configure PostgreSQL connection in backend/config.py

5. Create database and run schema:

    - psql -U youruser -d yourdb -f backend/db/schema.sql

6. Start API server:

    flask run


Frontend

1. Enter frontend folder:

    - cd frontend
    - npm install
  
2. Configure API endpoint in .env

3. Start frontend:

    - npm start

 
### Running Tests
Backend:

    - cd backend

    - pytest --cov=.


## API Documentation

| Endpoint                | Method   | Description                      |
| ----------------------- | -------- | -------------------------------- |
| `/api/v1/auth/register` | POST     | Create user account              |
| `/api/v1/auth/login`    | POST     | Authenticate & receive JWT       |
| `/api/v1/assets`        | GET      | List assets (with search/filter) |
| `/api/v1/assets`        | POST     | Create new asset                 |
| `/api/v1/assets/:id`    | GET      | Retrieve specific asset          |
| `/api/v1/assets/:id`    | PUT      | Update asset details             |
| `/api/v1/assets/:id`    | DELETE   | Delete an asset                  |
| `/api/v1/projects`      | GET/POST | Manage projects                  |
| `/api/v1/tags`          | GET/POST | Manage tags                      |
| `/api/v1/types`         | GET/POST | Manage asset types               |

## Architecture & Directory Layout

backend/
├─ app/
│  ├─ init.py        # App factory & blueprint setup
│  ├─ api/           # Route definitions per module
│  ├─ core/          # Config & shared logic
│  ├─ db/            # DB connection & enums
│  ├─ schemas/       # Pydantic data validation models
│  └─ test/          # Unit and integration tests
frontend/
└─ src/
   ├─ components/
   ├─ services/      # API call logic
   └─ App.jsx
docker-compose.yml


## Development Workflow

1. Clone and install dependencies
2. Activate backend and configure DB
3. Containerize or run services manually
4. Build features in backend or React UI
5. Write tests for every route/component enhancement
6. Run pytest + code coverage
7. Deploy via Docker or host backend/frontend separately

## Future Improvements

- Role-based access control (RBAC)

- Frontend pagination and sorting

- OpenAPI/Swagger auto-generated API docs

- CI pipeline (Test coverage)

- MongoDB or Redis caching layer

- Asset import/export via CSV

## Contact 
Maintainer: Zainab J.










