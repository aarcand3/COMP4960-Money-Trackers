import ollama
import sys

messages = []

def send(chat):
    messages.append({'role': 'user', 'content': chat})
    stream = ollama.chat(model='tinyllama', messages=messages, stream=True)

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        print(part, end='', flush=True)
        response += part

    messages.append({'role': 'assistant', 'content': response})

while True:
    chat = input("\n\n>>> ")
    if chat == "quit":
        print(messages)
        break
    elif len(chat) > 0:
        send(chat)