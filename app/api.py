import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("API_KEY")


model_id="openai/gpt-3.5-turbo"

def call_api(user_input,user_id=None,short_term_memory=None,long_term_memory=None):
  url="https://openrouter.ai/api/v1/chat/completions"


  headers={"Authorization":f"Bearer {api_key}",
            "Content-Type": "application/json"}

  messages=[{"role": "system", "content": "Your name is AshiAI and you are a helpful assistant."}]
  if short_term_memory:
    messages.extend(short_term_memory)

  messages.append({"role":"user",
                   "content":user_input})
  
  data={"model":model_id,
        "messages":messages,
  }

  try:
    response=requests.post(url,headers=headers,json=data)
    reply=response.json()
    if "choices" in reply and len(reply["choices"]) > 0:
      return reply["choices"][0]["message"]["content"]
      
    else:
      print("Unexpected API response:", reply)
      return "Sorry, I couldn't process your request."
  except Exception as e:
    print(f"Error calling API: {e}")
    return "I'm sorry, I'm having trouble processing your request. Please try again later."
  






