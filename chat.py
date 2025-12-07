import requests
def startChat(userMessage):
    URL = 'http://jld.ddns.net:11434/api/chat'
    model = 'gemma3:12b'
    messages = []
 
    # Check if server is up & reachablez
    try:
        response_check = requests.get(URL)
        if response_check.status_code != 200:
            return f"Error: Unable to reach the API, status code: {response_check.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: The AI server apears to be offline\nContact donahuej5@wit.edu"
        
        
    while True:
        user_input = userMessage
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
            "keep_alive":"3m",
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
        
        
