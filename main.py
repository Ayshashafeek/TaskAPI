from typing import Optional
from fastapi import FastAPI, Request, status
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