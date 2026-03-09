from pydantic import BaseModel

class YokaiCreate(BaseModel):
    name: str
    rank: str
    tribe: str
    attribute: str
    imageurl: str

class Yokai(BaseModel):
    id: int
    name: str
    rank: str
    tribe: str
    attribute: str
    imageurl: str