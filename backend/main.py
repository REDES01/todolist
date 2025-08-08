from http.client import HTTPException

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session,selectinload
import models, schemas, AI
from database import engine,SessionLocal, Base

from starlette.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/todos")
def read_todos(db: Session = Depends(get_db)):
    todos = db.query(models.Todo).options(selectinload(models.Todo.subtasks)).all()
    return todos

@app.get("/todos/{id}/subtasks")
def read_todo(id: int, db: Session = Depends(get_db)):
    todo=db.get(models.Todo,id)
    if not todo:
        raise HTTPException(404, "todo not found")

    return todo.subtasks

@app.post("/todos")
def add_todo(todo:schemas.Todo,db: Session = Depends(get_db)):
    db_to=models.Todo(
        content=todo.content,
        is_done=todo.is_done,
        end_date=todo.end_date
    )
    db.add(db_to)
    db.commit()
    db.refresh(db_to)
    return db_to

@app.post("/todos/{id}/subtasks")
def add_subtask(subtask:schemas.Subtask,id:int,db: Session = Depends(get_db)):
    todo = db.get(models.Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")

    db_subtask=models.Subtask(content=subtask.content,is_done=subtask.is_done)
    todo.subtasks.append(db_subtask)

    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

@app.post("/todos/{id}/subtasks/generate")
def generate_subtask(id:int,db: Session = Depends(get_db)):
    todo = db.get(models.Todo, id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    subtasks=AI.generate_subtask(todo.content)

    for subtask in subtasks:
        db_subtask=models.Subtask(content=subtask.content,is_done=subtask.is_done)
        todo.subtasks.append(db_subtask)
        db.add(db_subtask)

    db.commit()
    db.refresh(todo)

    return subtasks

@app.put("/todos/{id}")
def update_todo(new_todo:schemas.Todo,id:int,db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter_by(id=id).first()
    if todo:
        todo.content=new_todo.content
        todo.is_done=new_todo.is_done
        todo.end_date=new_todo.end_date
        db.commit()
        return todo
    else:
        raise HTTPException(status_code=404,detail="not found")

@app.put("/subtasks/{subtask_id}")
def update_subtask(new_subtask:schemas.Subtask,subtask_id:int,db: Session = Depends(get_db)):

    subtask = db.query(models.Subtask).filter_by(id=subtask_id).first()
    if subtask:
        subtask.content = new_subtask.content
        subtask.is_done = new_subtask.is_done
        db.commit()
        return subtask
    else:
        raise HTTPException(status_code=404,detail="subtask not found")

@app.delete("/todos/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo=db.query(models.Todo).filter_by(id=id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return todo
    else:
        raise HTTPException(status_code=404,detail="not found")

@app.delete("/subtasks/{subtask_id}")
def delete_todo(subtask_id:int,db: Session = Depends(get_db)):
    subtask=db.query(models.Subtask).filter_by(id=subtask_id).first()
    if subtask:
        db.delete(subtask)
        db.commit()
    else:
        raise HTTPException(status_code=404,detail="subtask not found")






# @app.get("/todos/test")
# def read_todos_test(db: Session = Depends(get_db)):
#     todos= db.query(models.ToDo).all()
#
#     return [
#         {
#             "todo":todos.todo,
#             "username":todos.user.name
#         }
#         for todos in todos
#     ]

