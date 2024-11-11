import asyncio
from typing import Dict, List, Optional
from dotenv import load_dotenv

from llama_stack_client.lib.agents.agent import Agent
from llama_stack_client import LlamaStackClient
from llama_stack_client.types.agent_create_params import (
    AgentConfig,
    AgentConfigToolSearchToolDefinition
)
import os
from typing import IO
from io import BytesIO
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import websockets
import json
from termcolor import cprint


load_dotenv()

# eleven = AsyncElevenLabs(
#   api_key=os.getenv(ELEVENLABS_API_KEY)
# )
ELEVENLABS_API_KEY="sk_e15987640cffeb0e339b0717b33cc0eaef69dafe9620857b"

# async def print_models() -> None:
#     models = await eleven.models.get_all()
#     print(models)

# asyncio.run(print_models())

# llama_server_ip = os.getenv(LLAMA_STACK_SERVER)  # Replace with your host
# llama_server_port = os.getenv(LLAMA_STACK_SERVER_PORT)       # Replace with your port
llama_server_ip = "localhost"  # Replace with your host
llama_server_port = 5000       # Replace with your port

client = LlamaStackClient(base_url=f'http://{llama_server_ip}:{llama_server_port}')
eleven_labs_client = ElevenLabs(
    api_key=ELEVENLABS_API_KEY,
)
voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
model_id="eleven_multilingual_v2"

conversation_history = []
in_messages = []

async def start_conversation_with(user_id: int, persona: str = ''):
    # TODO: not used at the moment
    set_system_persona = {"role": "system", "content": f"You are speaking as {persona}. Based on what you know about this person, respond to the following question: [User question]. Try to be concise and limit your response to 50 words max. If the question is in a different language, respond in that language. But first, confirm to the user that you're who you are in the first response."}
    # set_system_persona = {"role": "system", "content": f"You are {persona} who gives helpful advices."}
    in_messages.append(set_system_persona)
    message = {"role": "user", "content": "Hi"}
    in_messages.append(message)
    response = client.inference.chat_completion(
        messages=in_messages,
        model='Llama3.2-3B-Instruct',
    )
    resp = response.completion_message.content
    cprint(f'> {persona}: {resp}', 'cyan')

def chat():
    # few_shot_examples = [
    #     {"role": "user", "content": 'The llama hackathon is ending in one day.'},
    #     {
    #         "role": "assistant",
    #         "content": "Don't cry because it's over. Smile because it happened!",
    #         "stop_reason": 'end_of_message',
    #         "tool_calls": []
    #     },
    #     {
    #         "role": "user",
    #         "content": "I feel lost."
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "You’re on your own. And you know what you know. And you are the one who’ll decide where to go",
    #         "stop_reason": 'end_of_message',
    #         "tool_calls": []
    #     },
    #     {
    #         "role": "user",
    #         "content": "It's not worth it. Let's use something else."
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "So be sure when you step, Step with care and great tact. And remember that life is a great balancing act.",
    #         "stop_reason": 'end_of_message',
    #         "tool_calls": []
    #     },
    #     {
    #         "role": "user",
    #         "content": "What color is egg?"
    #     },
    #     {
    #         "role": "assistant",
    #         "content": "Why, of course. It's green.",
    #         "stop_reason": 'end_of_message',
    #         "tool_calls": []
    #     }
    # ]

    # in_messages.extend(few_shot_examples)
    while True:
        user_input = input('User> ')
        if user_input.lower() in ['exit', 'quit', 'bye']:
            resp = 'Ending conversation. Goodbye!', 'yellow'
            return resp

        message = {"role": "user", "content": user_input}
        in_messages.append(message)
        response = client.inference.chat_completion(
            messages=in_messages,
            model='Llama3.2-3B-Instruct',
        )
        resp = response.completion_message.content
        cprint(f'> {persona}: {resp}', 'cyan')
        text_to_speech_stream(resp)
        # Append the assistant message with all required fields
        assistant_message = {
            "role": "user",
            "content": resp,
            # Add any additional required fields here if necessary
        }
        conversation_history.append(assistant_message)
    return resp

# async def text_to_speech_streaming(voice_id: int, model_id: int, text: str):
#     uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}"
#     await websockets.send(json.dumps({
#             "text": " ",
#             "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": False},
#             "generation_config": {
#                 "chunk_length_schedule": [120, 160, 250, 290]
#             },
#             "xi_api_key": ELEVENLABS_API_KEY,
#         }))
#     await websockets.send(json.dumps({"text": text}))

#     # Send empty string to indicate the end of the text sequence which will close the websocket connection
#     await websockets.send(json.dumps({"text": ""}))

    
async def write_to_local(audio_stream):
    """Write the audio encoded in base64 string to a local mp3 file."""

    with open(f'./output/test.mp3', "wb") as f:
        async for chunk in audio_stream:
            if chunk:
                f.write(chunk)

async def listen(websocket):
    """Listen to the websocket for audio data and stream it."""

    while True:
        try:
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("audio"):
                yield base64.b64decode(data["audio"])
            elif data.get('isFinal'):
                break

        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break

# async def text_to_speech_ws_streaming(voice_id, model_id):
#     uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id={model_id}"
#     async with websockets.connect(uri) as websocket:
#           ...
#           # Add listen task to submit the audio chunks to the write_to_local function
#           listen_task = asyncio.create_task(write_to_local(listen(websocket)))

#           await listen_task

# asyncio.run(text_to_speech_ws_streaming(voice_id, model_id))

def text_to_speech_stream(text: str):
    # Perform the text-to-speech conversion
    response = eleven_labs_client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    import uuid
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    # from pydub import AudioSegment  
    # from pydub.playback import play
    # mp3_file = AudioSegment.from_file(file = save_file_path,  
    #                               format = "mp3")  
    # play(mp3_file)
    print(f"{save_file_path}: A new audio response was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

    # Create a BytesIO object to hold the audio data in memory
    # audio_stream = BytesIO()

    # # Write each chunk of audio data to the stream
    # for chunk in response:
    #     if chunk:
    #         audio_stream.write(chunk)

    # # Reset stream position to the beginning
    # audio_stream.seek(0)

    # # Return the stream for further use
    # return audio_stream
# To run it in a python file, use this line instead
def is_valid_person_name(name: str) -> bool:
    return all(x.isalpha() or x.isspace() for x in name)

if __name__ == "__main__":
    import re
    i = 0
    persona = "Dr. Seuss"
    while i < 3:
        cprint(f'> Hmm, remind me. Who am I?', 'cyan')
        user_input = input('User> ')
        if is_valid_person_name(user_input):
            persona = user_input.title()
            # cprint(f"> Aha, I'm {persona}", 'cyan')
            asyncio.run(start_conversation_with(1, persona))
            break
        if i == 3:
            # cprint(f"> Seems like you can't make up your mind. I'll be {persona.title()}", 'cyan')
            asyncio.run(start_conversation_with(1, persona))
    chat()

