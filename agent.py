from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = []

def chat(user_message: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an intelligent AI Agent built for Skysecure.
                You analyze queries, break them into steps, and provide structured
                professional responses. Always be precise and actionable."""
            },
            *conversation_history
        ]
    )

    reply = response.choices[0].message.content
    reply = re.sub(r'\*\*(.+?)\*\*', r'\1', reply)

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    if len(conversation_history) > 10:
        conversation_history.pop(0)
        conversation_history.pop(0)

    return reply