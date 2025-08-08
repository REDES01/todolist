import os

from openai import OpenAI
from pydantic import BaseModel
from typing import List


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

client=OpenAI(api_key=OPENAI_API_KEY)

class Subtask(BaseModel):
    content:str
    is_done:bool=False
class Subtasks(BaseModel):
    subtasks: List[Subtask]

def generate_subtask(content:str):
    completion = client.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Given the task, break it down to subtasks. Stay simple."},
            {"role": "user", "content": content},
        ],
        response_format=Subtasks,
    )

    subtasks = completion.choices[0].message.parsed.subtasks

    return subtasks

