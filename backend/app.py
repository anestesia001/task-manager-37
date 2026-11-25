import logging

import pymysql
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Literal
from contextlib import closing

from database import get_connection


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Task Manager API")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(default="", max_length=5000)


class TaskUpdate(BaseModel):
    status: Literal["pending", "in_progress", "done"]


@app.exception_handler(pymysql.MySQLError)
async def database_error_handler(request, exc):
    logger.error("Database error: %s", exc)

    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable"}
    )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "backend"
    }


@app.get("/ready")
def readiness():
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM tasks LIMIT 1")

    return {
        "status": "ready",
        "database": "connected"
    }


@app.get("/tasks")
def get_tasks():
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tasks ORDER BY id DESC"
            )
            return cursor.fetchall()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM tasks WHERE id = %s",
                (task_id,)
            )

            task = cursor.fetchone()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                """,
                (task.title, task.description)
            )

            task_id = cursor.lastrowid

    logger.info("Task created: id=%s", task_id)

    return {
        "id": task_id,
        "message": "Task created"
    }


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM tasks WHERE id = %s",
                (task_id,)
            )

            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            cursor.execute(
                """
                UPDATE tasks
                SET status = %s
                WHERE id = %s
                """,
                (task.status, task_id)
            )

    logger.info("Task updated: id=%s", task_id)

    return {"message": "Task updated"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM tasks WHERE id = %s",
                (task_id,)
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

    logger.info("Task deleted: id=%s", task_id)

    return {"message": "Task deleted"}


@app.get("/stats")
def get_stats():
    with closing(get_connection()) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM tasks
                GROUP BY status
                """
            )

            rows = cursor.fetchall()

    stats = {
        "pending": 0,
        "in_progress": 0,
        "done": 0
    }

    for row in rows:
        stats[row["status"]] = row["count"]

    stats["total"] = sum(stats.values())

    return stats