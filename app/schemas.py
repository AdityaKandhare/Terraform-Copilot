from pydantic import BaseModel

class GenerateResponse(BaseModel):
    terraform: str

class FixResponse(BaseModel):
    result: str

class CodeInput(BaseModel):
    code: str