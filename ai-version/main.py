from typing import List, Optional

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI(title="Task API", version="1.0")

# In-memory storage
_tasks: List[dict] = []
_next_id = 1


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int


def _find_task_index(task_id: int) -> Optional[int]:
    for i, t in enumerate(_tasks):
        if t["id"] == task_id:
            return i
    return None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global _next_id
    item = task.dict()
    item["id"] = _next_id
    _next_id += 1
    _tasks.append(item)
    return item


@app.get("/tasks", response_model=List[Task])
def list_tasks():
    return _tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    idx = _find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[idx]


@app.put("/tasks/{task_id}", response_model=Task)
def replace_task(task_id: int, task: TaskCreate):
    idx = _find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    item = task.dict()
    item["id"] = task_id
    _tasks[idx] = item
    return item


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate):
    idx = _find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    stored = _tasks[idx]
    update_data = task.dict(exclude_unset=True)
    for k, v in update_data.items():
        stored[k] = v
    _tasks[idx] = stored
    return stored


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    idx = _find_task_index(task_id)
    if idx is None:
        raise HTTPException(status_code=404, detail="Task not found")
    _tasks.pop(idx)
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
