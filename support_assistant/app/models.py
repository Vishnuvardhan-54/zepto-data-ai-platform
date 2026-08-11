# pyrefly: ignore [missing-import]
from pydantic import BaseModel

# Define the input format for the /ask endpoint
class AskRequest(BaseModel):
    query: str

# Define the output format returned by the /ask endpoint
class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float