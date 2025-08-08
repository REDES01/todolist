from datetime import datetime

from pydantic import BaseModel


class Todo(BaseModel):
    content:str
    is_done:bool
    end_date:datetime

class Subtask(BaseModel):
    content:str
    is_done:bool=False