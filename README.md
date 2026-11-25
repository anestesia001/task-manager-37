# Task Manager — DevOps Training Project

Приложение для управления задачами.

## Стек технологий

- Backend — Python, FastAPI, Uvicorn.
- Frontend — Python, Flask, Jinja2, Gunicorn.
- Database — MariaDB.
- Communication — REST API, HTTP, JSON.

## Доступ к приложению

| Компонент | Адрес |
|---|---|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| OpenAPI | http://localhost:8000/openapi.json |


## API Endpoints

| Метод | Endpoint | Описание |
|---|---|---|
| GET | /health | Проверка состояния Backend |
| GET | /ready | Проверка доступности БД |
| GET | /tasks | Получение всех задач |
| GET | /tasks/{id} | Получение задачи |
| POST | /tasks | Создание задачи |
| PATCH | /tasks/{id} | Изменение статуса |
| DELETE | /tasks/{id} | Удаление задачи |
| GET | /stats | Получение статистики |

## Примеры работы с API

Получить список задач:

```bash
curl http://localhost:8000/tasks
```

Создать задачу:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Configure CI/CD",
    "description": "Create GitLab pipeline"
  }'
```

Получить задачу:

```bash
curl http://localhost:8000/tasks/1
```

Изменить статус:

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

Удалить задачу:

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

Получить статистику:

```bash
curl http://localhost:8000/stats
```

## Проверка состояния приложения

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready

curl http://localhost:8000/health
curl http://localhost:8000/ready
```
