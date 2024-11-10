from pydantic import BaseModel

# model for chatbot persona
class Persona(BaseModel):
    name: str
    input: int