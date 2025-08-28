# Backend Service

This service contains the core business logic, API gateway, and session management for the intelligent conversation agent system.

## Structure

The service follows a Domain-Driven Design (DDD) approach:
- **`app/interfaces`**: FastAPI endpoints and data schemas.
- **`app/application`**: Application services that orchestrate the business logic.
- **`app/domain`**: The core of the application, including models, repository interfaces, and domain services.
- **`app/infrastructure`**: Concrete implementations of repositories and other infrastructure concerns.

## Running the Service

- **Production**: `sh run.sh`
- **Development**: `sh dev.sh`
