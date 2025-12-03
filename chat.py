import requests
def startChat():
    URL = 'http://jld.ddns.net:11434/api/chat'
    model = 'gemma3:12b'
    messages = []

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
            "keep_alive":"5m",
        }

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(URL, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            reply = response_data['message']['content']
        
            if reply:
                return reply
            else:
                return None
            
        else:
            return(f"Error: {response.status_code} - {response.text}")
        
        
