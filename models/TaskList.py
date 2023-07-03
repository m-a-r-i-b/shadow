from typing import List

from models.Task import Task
from pydantic import BaseModel


class TaskList(BaseModel):
  
    taskList: List[Task]

    def __iter__(self):
        return iter(self.taskList)

    def __getitem__(self, item):
        return self.taskList[item]