from typing import Optional
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


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

tasks = [
    {"id": 1, "title": "Complete assignment", "done": False},
    {"id": 2, "title": "Study FastAPI", "done": True},
    {"id": 3, "title": "Push code to GitHub", "done": False},
]


@app.get("/")
def root():
  return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
def health():
  return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
  return tasks


@app.get("/tasks/{id}")
def get_task(id: int):
  for task in tasks:
    if task["id"] == id:
      return task

  return JSONResponse(
      status_code=404, content={"error": f"Task {id} not found"}
  )


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
  if task.title is None or task.title.strip() == "":
    return JSONResponse(status_code=400, content={"error": "Title is required"})

  new_task = {"id": len(tasks) + 1, "title": task.title, "done": False}

  tasks.append(new_task)

  return new_task
@app.put("/tasks/{id}")
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
@app.delete("/tasks/{id}", status_code=204)
def delete_task(id: int):

    for index, task in enumerate(tasks):
        if task["id"] == id:
            tasks.pop(index)
            return Response(status_code=204)

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"},
    )