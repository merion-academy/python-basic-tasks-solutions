# Задание №6
## Асинхронное веб-приложение на FastAPI с использованием SQLAlchemy. Взаимодействие с внешним API и базой данных в асинхронном режиме.

Создание конфигурации `alembic` с поддержкой асинхронного движка:
```shell
alembic init -t async alembic
```

Запуск сервиса Postgres:
```shell
docker compose up -d pg
```

Остановка сервиса Postgres:
```shell
docker compose stop pg
```
