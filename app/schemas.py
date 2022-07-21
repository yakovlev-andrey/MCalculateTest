import enum
from pydantic import BaseModel

from celery.states import PRECEDENCE

State = enum.Enum("State", {state: state for state in PRECEDENCE if state is not None})


class Task(BaseModel):
    task_id: str
    state: State
    result: str | None


class TaskCreated(BaseModel):
    task_id: str


class Operation(enum.Enum):
    PLUS = "+"
    MINUS = "-"
    DIVIDE = "/"
    MULTIPLY = "*"


class StrictInt(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, float):
            raise TypeError("Will not coerce float to int")
        return v


class Calculate(BaseModel):
    x: StrictInt
    y: StrictInt
    operation: Operation
