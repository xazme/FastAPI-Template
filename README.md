# FastAPI Template
Простой шаблон для проектов на FastAPI.
## Запуск
```shell
# Создаем приватные и публичные ключи
mkdir -p certs/jwt/{access_keys,refresh_keys}
openssl genrsa -out certs/jwt/access_keys/private.pem 2048
openssl rsa -in certs/jwt/access_keys/private.pem -pubout -out certs/jwt/access_keys/public.pem
openssl genrsa -out certs/jwt/refresh_keys/private.pem 2048
openssl rsa -in certs/jwt/refresh_keys/private.pem -pubout -out certs/jwt/refresh_keys/public.pem

# Запускаем
docker compose up -d
```
Работает только в Docker или на UNIX системе из-за uvloop.
## Что умеет
* Базовая структура проекта (router / service / repository)
* JWT-аутентификация
* Пользователи (CRUD)
* Async SQLAlchemy + PostgreSQL
* Alembic миграции
* Dependency Injection (dishka)
* Настроенный линтер и типизация
* Базовая тестовая конфигурация
## Основные зависимости / компоненты
### Backend
* fastapi
* sqlalchemy (asyncio)
* pydantic
* pydantic-settings
* uvicorn
* gunicorn
* alembic
* pyjwt
* bcrypt
* cryptography
* faststream (kafka)
* dishka
* dishka-faststream
### Инструменты разработки
* ruff
* pyright
* pytest
### Аля-деплой
* Docker
Используется **uv** для управления зависимостями.

