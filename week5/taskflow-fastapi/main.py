from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tasks.db"

Priority = Literal["Low", "Medium", "High"]
Category = Literal["Reading", "Coding", "Writing", "Review"]


class TaskIn(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    category: Category = "Reading"
    priority: Priority = "Medium"
    notes: str = Field(default="", max_length=220)
    done: bool = False


class Task(TaskIn):
    id: int


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL CHECK (length(title) >= 3),
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            conn.execute(
                """
                INSERT INTO tasks (title, category, priority, notes, done)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    "Run the FastAPI version",
                    "Coding",
                    "High",
                    "Use uvicorn, then test the API-backed CRUD flow.",
                    0,
                ),
            )


def row_to_task(row: sqlite3.Row) -> Task:
    return Task(
        id=row["id"],
        title=row["title"],
        category=row["category"],
        priority=row["priority"],
        notes=row["notes"],
        done=bool(row["done"]),
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Study Task Board API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [row_to_task(row) for row in rows]


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(task: TaskIn) -> Task:
    with connect() as conn:
        cursor = conn.execute(
            """
            INSERT INTO tasks (title, category, priority, notes, done)
            VALUES (?, ?, ?, ?, ?)
            """,
            (task.title.strip(), task.category, task.priority, task.notes.strip(), int(task.done)),
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return row_to_task(row)


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskIn) -> Task:
    with connect() as conn:
        existing = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Task not found")
        conn.execute(
            """
            UPDATE tasks
            SET title = ?, category = ?, priority = ?, notes = ?, done = ?
            WHERE id = ?
            """,
            (
                task.title.strip(),
                task.category,
                task.priority,
                task.notes.strip(),
                int(task.done),
                task_id,
            ),
        )
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return row_to_task(row)


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    with connect() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Task not found")
