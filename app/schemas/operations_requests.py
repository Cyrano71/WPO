from pydantic import BaseModel
from typing import Dict

class Priority(BaseModel):
    value: int

class OperationDataRequest(BaseModel):
    _id: str
    name: str
    priority: Priority
    restrictions: list[object]

class MeteoArgument(BaseModel):
    town: str

class RequestArguments(BaseModel):
    level: int
    meteo: MeteoArgument

class PriorityDataGetRequest(BaseModel):
    operation_name: str
    arguments: RequestArguments