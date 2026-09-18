from ollama import chat

response = chat(
    model="gemma3",
    messages=[
        {
            "role": "user",
            "content": "You are an IT support assistant. Explain in one sentence what to check when a laptop touchpad stops working."
        }
    ]
)

print("\nAI RESPONSE:\n")
print(response.message.content)