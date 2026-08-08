# Task API

A simple RESTful CRUD API built with **FastAPI** for managing tasks.

## Features

- Create a task
- View all tasks
- View a task by ID
- Update a task
- Delete a task
- Filter tasks by completion status
- Search tasks by title
- View task statistics
- Interactive Swagger UI documentation
- In-memory task storage

---

## Tech Stack

- Python 3
- FastAPI
- Uvicorn
- Pydantic

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Ayshashafeek/TaskAPI.git
cd TaskAPI
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install fastapi uvicorn
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get task by ID |
| POST | `/tasks` | Create a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |
| GET | `/tasks?done=true` | Filter tasks by completion status |
| GET | `/tasks?search=FastAPI` | Search tasks by title |
| GET | `/stats` | Get task statistics |

---

## Example curl

```bash
curl -i http://127.0.0.1:8000/tasks
```

Example output:

```http
HTTP/1.1 200 OK
content-type: application/json

[
  {
    "id": 1,
    "title": "Complete assignment",
    "done": false
  },
  {
    "id": 2,
    "title": "Study FastAPI",
    "done": true
  }
]
```

---

## Swagger UI

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows the API endpoints to be tested directly from the browser without using curl.

---

## Screenshots

### Swagger UI

![Swagger UI](docs/swagger-ui.png)

### Create Task

![Create Task](docs/create-task.png)

### Get Tasks

![Get Tasks](docs/get-tasks.png)

---

## Persistence Experiment

Tasks created through the API disappear when the server is restarted. This happens because the current Task API stores tasks only in an in-memory Python list rather than a persistent database. The data therefore exists only while the application process is running.

---

# AI vs Me

For Stage 7, I asked an AI assistant to independently build the same Task API based on my own specification. The generated implementation was kept separate from the hand-built Stage 0–6 implementation.

## My Original Prompt

> Build a REST API for managing tasks using Python and FastAPI. Store the tasks in memory using a Python list, without a database. I need endpoints for creating, reading, updating, and deleting tasks. The API should validate request bodies, return appropriate HTTP status codes, handle missing task IDs, and expose Swagger documentation. Make the API runnable with Uvicorn.

The AI-generated version was tested separately using Swagger UI and compared with my hand-built implementation.

## Differences I Found

### 1. Task Structure

My implementation uses:

```json
{
  "id": 1,
  "title": "Study FastAPI",
  "done": true
}
```

The AI implementation used:

```json
{
  "id": 1,
  "title": "aysh",
  "description": "a girl",
  "completed": false
}
```

The AI added a `description` field and used `completed` instead of `done`.

**Reason:** My prompt did not explicitly specify the exact task schema, so the AI made its own design decision.

### 2. Extra PATCH Endpoint

My API requires:

```text
PUT /tasks/{id}
```

for updating tasks.

The AI implementation provided both:

```text
PUT /tasks/{task_id}
PATCH /tasks/{task_id}
```

PATCH was not required.

**Reason:** My prompt requested CRUD and an update operation but did not explicitly say that PUT must be the only update endpoint.

### 3. Error Response Format

My implementation returns a custom response for an unknown task:

```json
{
  "error": "Task 99 not found"
}
```

The AI implementation returned:

```json
{
  "detail": "Task not found"
}
```

The structure and message were different.

**Reason:** My prompt requested appropriate error handling but did not specify the exact JSON error format.

### 4. Validation Behavior

My implementation converts FastAPI request validation errors into HTTP `400` responses.

The AI-generated Swagger documentation showed FastAPI's default:

```text
422 Validation Error
```

**Reason:** My original prompt did not explicitly state that validation errors must return `400` instead of FastAPI's default `422`.

## What Did the AI Do Better?

The AI used separate Pydantic models such as `Task`, `TaskCreate`, and `TaskUpdate`, which made the API structure clear and strongly typed. Its generated Swagger documentation also clearly exposed the request and response schemas.

I could understand and explain these choices because I had already built the same API manually.

## What Did the AI Get Wrong?

The AI changed the task data model, added an unnecessary PATCH endpoint, and did not follow my intended custom error and validation behavior.

These differences did not necessarily make the AI implementation unusable, but they made it different from the API I intended to build.

## What Did My Prompt Forget?

My original prompt was too general. I did not specify:

- The exact task fields: `id`, `title`, and `done`
- That `description` should not exist
- That `PUT` should be the update endpoint
- That PATCH should not be added
- That invalid request bodies should return `400`
- The exact JSON structure for `404` errors
- The exact response behavior for `DELETE`

The AI silently made decisions about these unspecified details.

## Rematch

After reviewing the first AI implementation, I improved my specification by explicitly defining the task schema, update behavior, validation status codes, error response format, and DELETE behavior.

The improved prompt produced a version that was closer to my original implementation because the requirements were more precise.

---

## Project Structure

```text
TaskAPI/
├── main.py
├── README.md
├── docs/
│   ├── swagger-ui.png
│   ├── create-task.png
│   └── get-tasks.png
└── ai-version/
    └── main.py
```

---

## Author

**Aysha Shafeek M M**
