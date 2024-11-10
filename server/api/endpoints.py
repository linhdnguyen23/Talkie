from fastapi import APIRouter
from models.persona import Persona
from helpers.persona_services import start_conversation_with, chat
import logging

router = APIRouter()
logger = logging.getLogger('uvicorn.error')

@router.post("/select_persona/")
async def handle_persona_selection(persona: Persona):
    logger.debug(f'this is a debug message: {persona}')
    start_conversation_with(persona.name)
    return persona

@router.post("/chat/req/")
async def handle_persona_selection(persona: Persona):
    logger.debug(f'this is a debug message: {persona}')
    chat(persona.name)
    return persona

