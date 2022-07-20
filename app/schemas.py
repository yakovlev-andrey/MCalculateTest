import enum
from pydantic import BaseModel

from celery.states import PRECEDENCE

State = enum.Enum(
    'State', {
        state: state for state in PRECEDENCE if state is not None})


class Task(BaseModel):
    task_id: str
    state: State
    result: str | None


class TaskCreated(BaseModel):
    task_id: str


class Operation(enum.Enum):
    PLUS = '+'
    MINUS = '-'
    DIVIDE = '/'
    MULTIPLY = '*'


class Calculate(BaseModel):
    x: int
    y: int
    operation: Operation
