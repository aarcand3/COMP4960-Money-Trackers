import requests

URL = 'http://jld.ddns.net:11434/api/chat'
model = 'gemma3:12b'
messages = []

# Basic chat loop
while True:

    user_input = input(">>> ")
    
    message = {
        "role": "user",
        "content": user_input
    }
    
    messages.append(message)

    payload = {
        "model": model,
        "messages": messages,
        "think": False,
        "options": {},
        "stream": False,
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        reply = response_data['message']['content']
        
        if reply:
            print("\n", reply)
            messages.append({
                "role": "assistant",
                "content": reply
            })
        else:
            print("<<<ERROR>>> No response")
            
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
        