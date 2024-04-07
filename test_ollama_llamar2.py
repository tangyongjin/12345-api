from ollama import Client

client = Client(host="http://119.255.238.247:11434")
response = client.chat(
    model="llama2-chinese",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)
print(response["message"]["content"])
