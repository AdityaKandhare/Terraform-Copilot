from pydantic import BaseModel


class GenerateResponse(BaseModel):
    terraform: str


class FixResponse(BaseModel):
    result: str