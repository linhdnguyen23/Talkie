from fastapi import APIRouter
from models.persona import Persona
from helpers.persona_services import start_conversation
import logging

router = APIRouter()
logger = logging.getLogger('uvicorn.error')

@router.post("/select_persona/")
async def handle_persona_selection(persona: Persona):
    logger.debug(f'this is a debug message: {persona}')
    start_conversation(persona.name)
    return persona

