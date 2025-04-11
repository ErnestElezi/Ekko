from playsound import playsound
from ollama import chat
from ollama import ChatResponse

import TTS


def getLLMResponse(question):
    response: ChatResponse = chat(model='qwen2.5:0.5b', messages=[
        {
            'role': 'tool',
            'content': f'{question} Answer in 10 words or less.',
        },
    ])

    return response.message.content
