from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


todo_list: List[TodoItem] = []


@app.post("/todos/", response_model=TodoItem)
def create_todo_item(todo: TodoItem):
    if any(item.id == todo.id for item in todo_list):
        raise HTTPException(status_code=400, detail="Todo with this ID already exists.")
    todo_list.append(todo)
    return todo


@app.get("/todos/", response_model=List[TodoItem])
def get_todo_list():
    return todo_list


@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo_item(todo_id: int, todo: TodoItem):
    for item in todo_list:
        if item.id == todo_id:
            item.title = todo.title
            item.description = todo.description
            item.completed = todo.completed
            return item
    raise HTTPException(status_code=404, detail="Todo not found.")


@app.delete("/todos/{todo_id}", response_model=TodoItem)
def delete_todo_item(todo_id: int):
    for item in todo_list:
        if item.id == todo_id:
            todo_list.remove(item)
            return item
    raise HTTPException(status_code=404, detail="Todo not found.")
