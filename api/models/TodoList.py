from pydantic import BaseModel, Field
from uuid import UUID

class TodoList(BaseModel):
    id: UUID
    name: str

class TodoEnty(BaseModel):
    id: UUID
    name: str
    description: str
    list_id: UUID