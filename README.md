# Support Ticketing System API

A Django REST Framework application for managing customer support tickets related to orders. The project provides separate APIs for customers and support staff, supports ticket conversations, notifications, and includes a Docker-based deployment with Nginx as a reverse proxy.

## Features

* Customer ticket creation
* Customer and support message threads
* Admin ticket management
* Ticket filtering and ordering
* Driver information in ticket details
* Email notification support (console backend)
* SMS notification support (printed in console)
* OpenAPI / Swagger documentation
* Docker Compose deployment
* Nginx reverse proxy
* PostgreSQL database

## Tech Stack

* Python 3.11
* Django
* Django REST Framework
* PostgreSQL
* Gunicorn
* Nginx
* Docker & Docker Compose
* drf-spectacular (OpenAPI / Swagger)

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/erfanfekry/support_ticketing_system.git
cd support_ticketing_system
```

## Configure environment variables

Create a `.env` file in the project root.

Example:

```env
POSTGRES_DB=support_ticket_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
```

## Build and start the application

```bash
docker compose up --build
```

The application will automatically:

* Build the Docker images
* Start PostgreSQL
* Apply database migrations
* Collect static files
* Start Gunicorn
* Start Nginx

## Sample Data

A sample fixture is included to make it easy to evaluate the application without manually creating users, orders, drivers, and tickets.

After starting the containers, load the sample data:

```bash
docker compose exec web python manage.py loaddata seed_data
```

The fixture includes:

* 3 Sample customers
* A staff (admin) user
* Sample drivers
* 5 Orders in different statuses (e.g. preparation, shipped, delivered)
* 5 Support tickets
* Ticket conversations

This data allows all customer and admin endpoints to be exercised immediately through the API or Swagger UI.

> **Note:** If the database already contains data, loading the fixture may fail due to duplicate primary keys or unique constraints. For a fresh start, remove the existing database volume and recreate the containers before loading the fixture.

If needed, recreate the database with:

```bash
docker compose down -v
docker compose up --build
docker compose exec web python manage.py loaddata seed_data
```

### Test Credentials

| Role     | Username              | Password              |
| -------- | --------------------- | --------------------- |
| Admin    | `Admin`    | `Admin123456`    |
| Customer(1) | `Ali` | `User123456` |
| Customer(2) | `Shayan` | `User123456` |
| Customer(3) | `Zahra ` | `User123456` |


## Stop the application

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```


# Running the Project

## Prerequisites

* Docker
* Docker Compose

## Start the application

```bash
docker compose up --build
```

The application will automatically:

* Build the Docker images
* Start PostgreSQL
* Apply database migrations
* Collect static files
* Start Gunicorn
* Start Nginx

---

# API Documentation

After the application starts:

| Resource       | URL                          |
| -------------- | ---------------------------- |
| Swagger UI     | http://localhost/api/docs/   |
| OpenAPI Schema | http://localhost/api/schema/ |
| ReDoc          | http://localhost/api/redoc/  |

---

# Main Endpoints

## Customer

| Method | Endpoint                      | Description                 |
| ------ | ----------------------------- | --------------------------- |
| POST   | `/api/tickets/`               | Create a new support ticket |
| GET    | `/api/tickets/`               | List customer's tickets     |
| GET    | `/api/tickets/{id}/`          | Retrieve ticket details     |
| POST   | `/api/tickets/{id}/messages/` | Add a message to a ticket   |

## Admin

| Method | Endpoint                         | Description               |
| ------ | -------------------------------- | ------------------------- |
| GET    | `/api/admin/tickets/`            | List all tickets          |
| GET    | `/api/admin/tickets/{id}/`       | Retrieve ticket details   |
| POST   | `/api/admin/tickets/{id}/reply/` | Reply to a support ticket |

---

# Authentication

Customer endpoints require an authenticated customer.

Admin endpoints require an authenticated staff user.

---

# Notifications

Ticket replies trigger the notification service.

* Email notifications use Django's console email backend.
* SMS notifications are represented by the notification service and can be integrated with a real SMS provider.

---

# Deployment

The project is containerized using Docker Compose.

Services:

* Django application (Gunicorn)
* PostgreSQL
* Nginx reverse proxy

Nginx forwards API requests to Gunicorn and serves static files directly.

---

# Project Structure

```
.
├── apps/
├── config/
├── media/
├── nginx/
├── .dockerignore
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

# Design Notes

The project follows a layered architecture to separate responsibilities:

* **Views** handle HTTP requests and responses.
* **Serializers** serialize API data.
* **Selectors** encapsulate database queries.
* **Validators** Validate  API data.
* **Services** contain business logic such as creating ticket messages and sending notifications.

This structure keeps views lightweight, improves maintainability, and simplifies testing.
