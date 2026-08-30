from database import get_connection, init_db
from typing import Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    description="A simple CRUD API for managing tasks built with FastAPI.",
    version="1.0.0",
)
init_db()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
  return JSONResponse(
      status_code=status.HTTP_400_BAD_REQUEST,
      content={"error": "Invalid request payload", "details": exc.errors()},
  )


class TaskCreate(BaseModel):
  title: Optional[str] = None
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


@app.get(
    "/",
    summary="API information",
    description="Returns basic information about the Task API."
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get(
    "/health",
    summary="Health check",
    description="Checks the health of the API."
)
def health():
  return {"status": "ok"}


@app.get(
    "/tasks",
    summary="Get all tasks",
    description="Returns a list of all tasks."
)
def get_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None
):
    conn = get_connection()

    query = "SELECT * FROM tasks"
    conditions = []
    parameters = []

    if done is not None:
        conditions.append("done = ?")
        parameters.append(done)

    if search is not None:
        conditions.append("title LIKE ?")
        parameters.append(f"%{search}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor = conn.execute(query, parameters)

    tasks = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return tasks


@app.get(
    "/tasks/{id}",
    summary="Get a task by ID",
    description="Returns the task with the specified ID."
)
def get_task(id: int):
    conn = get_connection()

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    task = cursor.fetchone()

    conn.close()

    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {id} not found"}
        )

    return dict(task)


@app.post(
    "/tasks",
    status_code=201,
    summary="Create a new task",
    description="Creates a new task with the specified title."
)
def create_task(task: TaskCreate):
    if task.title is None or task.title.strip() == "":
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"}
        )

    conn = get_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )

    task_id = cursor.lastrowid

    conn.commit()

    cursor = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    )

    new_task = dict(cursor.fetchone())

    conn.close()

    new_task["done"] = bool(new_task["done"])

    return new_task

@app.put(
    "/tasks/{id}",
    summary="Update a task",
    description="Updates the task with the specified ID."
)
def update_task(id: int, updated_task: TaskUpdate):

    if updated_task.title is None and updated_task.done is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Request body cannot be empty"},
        )

    for task in tasks:
        if task["id"] == id:

            if updated_task.title is not None:
                if updated_task.title.strip() == "":
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Title is required"},
                    )

                task["title"] = updated_task.title

            if updated_task.done is not None:
                task["done"] = updated_task.done

            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"},
    )
@app.delete(
    "/tasks/{id}",
    status_code=204,
    summary="Delete a task",
    description="Deletes a task by its ID."
)
def delete_task(id: int):

    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"},
    )
@app.get("/stats")
def get_stats():
    total = len(tasks)
    done = sum(1 for task in tasks if task["done"])
    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }