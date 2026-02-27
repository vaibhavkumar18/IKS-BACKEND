import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3.1-8b-instruct"


async def base_agent(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 600,
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "IKS-Hackathon",
    }

   
    
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(URL, json=payload, headers=headers)
            r.raise_for_status() # This will catch 404, 401, 500 etc.
            
            return r.json()["choices"][0]["message"]["content"].strip()
            
    except httpx.HTTPStatusError as e:
        print(f"OpenRouter Error: {e.response.text}")
        # Raising an HTTPException ensures the CORS middleware still runs
        raise HTTPException(status_code=e.response.status_code, detail="AI Service Unavailable")
    except Exception as e:
        print(f"General Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")