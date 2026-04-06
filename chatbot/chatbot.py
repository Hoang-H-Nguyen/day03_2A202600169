import os
import time
from typing import Any, Callable
from openai import OpenAI

OPENAI_MODEL = "gpt-5.4-mini"

def streaming_chatbot() -> None:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            break

        history.append({"role": "user", "content": user_input})

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True
        )

        print("Assistant: ", end="", flush=True)
        assistant_response = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            assistant_response += delta

        history.append({"role": "assistant", "content": assistant_response})
        history = history[-6:]  # Keep only the last 3 turns

if __name__ == "__main__":
    streaming_chatbot()