# Support Ticketing System API

A Django REST Framework application for managing customer support tickets related to orders. The project provides separate APIs for customers and support staff, supports ticket conversations, notifications, and includes a Docker-based deployment with Nginx as a reverse proxy.

## Features

* Customer ticket creation
* Customer and support message threads
* Admin ticket management
* Ticket filtering and ordering
* Driver information in ticket details
* Email notification support (console backend)
* OpenAPI / Swagger documentation
* Docker Compose deployment
* Nginx reverse proxy
* PostgreSQL database

## Tech Stack

* Python 3.12
* Django
* Django REST Framework
* PostgreSQL
* Gunicorn
* Nginx
* Docker & Docker Compose
* drf-spectacular (OpenAPI / Swagger)

---

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
├── nginx/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md
```

---

# Design Notes

The project follows a layered architecture to separate responsibilities:

* **Views** handle HTTP requests and responses.
* **Serializers** validate and serialize API data.
* **Selectors** encapsulate database queries.
* **Services** contain business logic such as creating ticket messages and sending notifications.

This structure keeps views lightweight, improves maintainability, and simplifies testing.
