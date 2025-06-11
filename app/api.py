import requests
import os
from dotenv import load_dotenv
from app.models import LongTermMemory
from app import db

# Load the API key
load_dotenv()
api_key = os.getenv("API_KEY")
model_id = "openai/gpt-3.5-turbo"

def check_memory_worthy(user_input, reply):
    return "remember" in user_input.lower() or "remember" in reply.lower() or "prefer" in user_input.lower() or "prefer" in reply.lower()

def store_memory(user_id, user_input, reply=None):
    memory = LongTermMemory(content=user_input, user_id=user_id)
    db.session.add(memory)
    db.session.commit()

def call_api(user_input, user_id=None, short_term_memory=None, long_term_memory=None):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": "Your name is AshiAI and you are a helpful assistant."}]

# Inject long-term memory (LTM)
    if long_term_memory:
        for memory in long_term_memory[-5:]:  # Limit to latest 5 LTM items
            messages.append({
                "role": "system",
                "content": f"Remember this about the user: {memory['content']}"
            })


    if short_term_memory:
        messages.extend(short_term_memory)
    
    # ✅ Add user input to the conversation
    messages.append({"role": "user", "content": user_input})

    data = {
        "model": model_id,
        "messages": messages,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        reply = response.json()

       
        if "choices" in reply and len(reply["choices"]) > 0:
            bot_reply = reply["choices"][0]["message"]["content"]

            if check_memory_worthy(user_input, bot_reply):
                store_memory(user_id, user_input, bot_reply)

            return bot_reply
        else:
            print("Unexpected API response:", reply)
            return "Sorry, I couldn't process your request."
    except Exception as e:
        print(f"Error calling API: {e}")
        return "Sorry, something went wrong."

