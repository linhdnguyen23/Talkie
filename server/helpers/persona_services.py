import asyncio
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client import LlamaStackClient
from llama_stack_client.types.agent_create_params import (
    AgentConfig,
    AgentConfigToolSearchToolDefinition
)
from elevenlabs.client import AsyncElevenLabs

eleven = AsyncElevenLabs(
  api_key="sk_e15987640cffeb0e339b0717b33cc0eaef69dafe9620857b" # Defaults to ELEVEN_API_KEY
)

async def print_models() -> None:
    models = await eleven.models.get_all()
    print(models)

asyncio.run(print_models())
from termcolor import cprint

load_dotenv()
HOST = "localhost"  # Replace with your host
PORT = 5000       # Replace with your port

client = LlamaStackClient(base_url=f'http://{HOST}:{PORT}')

async def start_conversation(user_id: int, persona: str = ''):
    conversation_history = []
    in_messages = []
    # TODO: not used at the moment
    persona = "Dr. Seuss"
    set_system_persona = {"role": "system", "content": f"You are speaking as {persona}. Based on what you know about this person, respond to the following question: [User question]"}
    # set_system_persona = {"role": "system", "content": f"You are {persona} who gives helpful advices."}
    in_messages.append(set_system_persona)
    
    few_shot_examples = [
    {"role": "user", "content": 'The llama hackathon is ending in one day.'},
    {
        "role": "assistant",
        "content": "Don't cry because it's over. Smile because it happened!",
        "stop_reason": 'end_of_message',
        "tool_calls": []
    },
    {
        "role": "user",
        "content": "I feel lost."
    },
    {
        "role": "assistant",
        "content": "You’re on your own. And you know what you know. And you are the one who’ll decide where to go",
        "stop_reason": 'end_of_message',
        "tool_calls": []
    },
    {
        "role": "user",
        "content": "It's not worth it. Let's use something else."
    },
    {
        "role": "assistant",
        "content": "So be sure when you step, Step with care and great tact. And remember that life is a great balancing act.",
        "stop_reason": 'end_of_message',
        "tool_calls": []
    },
    {
        "role": "user",
        "content": "What color is egg?"
    },
    {
        "role": "assistant",
        "content": "Why, of course. It's green.",
        "stop_reason": 'end_of_message',
        "tool_calls": []
    }
]

    # in_messages.extend(few_shot_examples)
    while True:
        user_input = input('User> ')
        if user_input.lower() in ['exit', 'quit', 'bye']:
            cprint('Ending conversation. Goodbye!', 'yellow')
            break

        message = {"role": "user", "content": user_input}
        in_messages.append(message)
        response = client.inference.chat_completion(
            messages=in_messages,
            model='Llama3.2-3B-Instruct',
        )
        cprint(f'> Response: {response.completion_message.content}', 'cyan')
        # Append the assistant message with all required fields
        assistant_message = {
            "role": "user",
            "content": response.completion_message.content,
            # Add any additional required fields here if necessary
        }
        conversation_history.append(assistant_message)

# To run it in a python file, use this line instead
# asyncio.run(start_conversation(1))

