# Mek

> Backend API for Mekwerab — an e-commerce and community platform for Ethiopian Orthodox church products, services, and community interaction.

## Overview

Mek is the backend service powering Mekwerab.

The project was built to handle the core backend requirements of a real-world web application, including authentication, product management, search, cart and checkout workflows, order tracking, community features, notifications, and API integration with the frontend.

The backend is built with **Django** and **Django REST Framework**, with **PostgreSQL** as the primary database.

## Features

- JWT-based authentication
- User profiles
- Product browsing and search
- Product categories
- Shopping cart
- Checkout and order management
- Order tracking
- Community posts
- Comments and replies
- Voting
- Notifications
- RESTful API
- PostgreSQL database
- API testing with Postman
- Query-count testing and database optimization
- CORS configuration for frontend integration

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | PostgreSQL |
| API Testing | Postman |
| Frontend Integration | React, TypeScript |
| Version Control | Git |

## API Modules

The backend is organized around the main functionality of Mekwerab:

- **Authentication** — registration, login, JWT authentication
- **Products** — products, categories, search
- **Cart** — cart and cart items
- **Orders** — checkout, orders, order tracking
- **Community** — posts, comments, replies, voting
- **Notifications** — user notifications
- **Profiles** — user profile information

## Database & Performance

Database performance was considered during development, including:

- Query-count testing
- Reducing unnecessary database queries
- Avoiding N+1 query patterns
- Efficient Django ORM usage
- Database indexing where appropriate

## Testing

API endpoints were tested using **Postman** during development.

Testing included:

- Authentication and authorization
- CRUD operations
- API permissions
- Cart and order workflows
- Community interactions
- Error handling
- Database query performance

## Frontend

The Mekwerab frontend is built separately using **React, TypeScript, Vite, and Tailwind CSS**.

The frontend communicates with this backend through the REST API.

**Frontend repository:**  
https://github.com/IyosiTes/Mek-Front

## Project Status

**Active development**

Mek is a real-world product-building project used to apply backend engineering, API development, database design, testing, and deployment concepts.

## Author

**Eyosias Tesfaye**

Backend-focused Full-Stack Developer & Product Builder
