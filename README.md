# FastAPI Template

Production-ready FastAPI template with JWT authentication, clean architecture, and best practices.

## Quick Start

```bash
git clone <your-repository>
cd app

# Install dependencies
poetry install

# Setup environment
cp .env.example .env

# Generate JWT keys
mkdir -p certs/jwt/{access_keys,refresh_keys}
openssl genrsa -out certs/jwt/access_keys/private.pem 2048
openssl rsa -in certs/jwt/access_keys/private.pem -pubout -out certs/jwt/access_keys/public.pem
openssl genrsa -out certs/jwt/refresh_keys/private.pem 2048
openssl rsa -in certs/jwt/refresh_keys/private.pem -pubout -out certs/jwt/refresh_keys/public.pem

# Run
poetry run uvicorn main:app --reload
```

API Documentation: http://localhost:8000/docs

## What's Included

### Ready-to-use Features
- **Authentication** (`/api/auth/...`)
  - `POST /register` - User registration
  - `POST /login` - Login with JWT tokens
  - `POST /refresh` - Refresh access token
  - `POST /logout` - Logout (token invalidation)

- **Users** (`/api/user/...`)
  - `GET /all` - List all users
  - `GET /{id}` - Get user by ID
  - `PATCH /{id}` - Update user
  - `DELETE /{id}` - Delete user

- **Core Architecture**
  - `BaseRepository` - Generic repository pattern
  - `BaseService` - Business logic layer
  - Async SQLAlchemy 2.0 with PostgreSQL
  - Dependency injection system
  - Centralized error handling
  - CORS middleware

## Adding New Modules

### 1. Create Module Structure
```
api/
└── product/                    # Your module name
    ├── __init__.py
    ├── models.py              # SQLAlchemy models
    ├── dto.py                # Pydantic schemas
    ├── repository.py         # Inherit from BaseRepository
    ├── service.py           # Inherit from BaseService
    ├── dependencies.py      # Dependency injection
    └── router.py           # API endpoints
```

### 2. Implementation Example

**`api/product/models.py`**
```python
from app.database import Base, CreatedAtMixin

class Product(Base, CreatedAtMixin):
    name: Mapped[str]
    price: Mapped[float]
```

**`api/product/dto.py`**
```python
from pydantic import BaseModel
from uuid import UUID

class ProductCreateDTO(BaseModel):
    name: str
    price: float

class ProductResponseDTO(BaseModel):
    id: UUID
    name: str
    price: float
    created_at: datetime
```

**`api/product/repository.py`**
```python
from app.shared import BaseRepository

class ProductRepository(BaseRepository[Product]):
    def __init__(self, session):
        super().__init__(model=Product, session=session)
```

**`api/product/service.py`**
```python
from app.shared import BaseService

class ProductService(BaseService[Product]):
    def __init__(self, repository, session):
        super().__init__(repository=repository, session=session)
```

**`api/product/dependencies.py`**
```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import db_helper
from .repository import ProductRepository
from .service import ProductService

def get_product_service(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> ProductService:
    repository = ProductRepository(session=session)
    return ProductService(repository=repository, session=session)

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]
```

**`api/product/router.py`**
```python
from fastapi import APIRouter, status
from typing import Annotated
from uuid import UUID
from .dependencies import ProductServiceDep
from .dto import ProductCreateDTO, ProductResponseDTO

router = APIRouter()

@router.post("/", 
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateDTO,
    service: ProductServiceDep,
):
    return await service.create(payload.model_dump())

@router.get("/", 
    response_model=list[ProductResponseDTO])
async def get_products(service: ProductServiceDep):
    return await service.get_all()

@router.get("/{product_id}", 
    response_model=ProductResponseDTO)
async def get_product(
    product_id: UUID,
    service: ProductServiceDep,
):
    return await service.get_one(id=product_id)
```

### 3. Register in `api/__init__.py`
```python
from .product.router import router as product_router

router.include_router(
    router=product_router,
    prefix="/products",
    tags=["Products"],
)
```

## Available BaseService Methods

```python
# Get data
await service.get(id=1)                     # By ID
await service.get_one(email="test@mail.ru") # By condition
await service.get_all()                     # All records
await service.get_all_filtered(active=True) # Filtered

# Create
await service.create({"name": "Test"})

# Update
await service.update_by_id(id=1, {"name": "Updated"})
await service.update(payload={"name": "New"}, email="test@mail.ru")

# Delete
await service.delete_by_id(id=1)
await service.delete(email="test@mail.ru")

# Utilities
exists = await service.exists(email="test@mail.ru")
count = await service.count()
```

## Project Structure
```
app/
├── api/                      # Business modules
│   ├── auth/                # Authentication (ready)
│   ├── user/                # Users (ready)
│   └── [your_module]/       # Your modules here
├── shared/                  # BaseRepository, BaseService
├── database/               # DB connection, models
├── config/                # Settings from .env
├── middlewares/           # CORS middleware
├── exception_handlers/    # Error handling
├── lifespan.py           # App lifecycle
├── main.py              # App factory
└── pyproject.toml       # Poetry dependencies
```

## Development Commands

```bash
# Install new package
poetry add <package-name>

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Check types
poetry run mypy .
```

---

**Ready to use.** Add your modules following the pattern above.