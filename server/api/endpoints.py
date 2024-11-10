from fastapi import APIRouter
from models.persona import Persona
from helpers.persona_services import start_conversation

router = APIRouter()

@router.post("/select_persona/")
async def handle_persona_selection(persona: Persona):
    return start_conversation(persona.name)
