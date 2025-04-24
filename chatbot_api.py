from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# CORS settings (optional for mobile frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "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"  # Replace this!
MODEL = "mistralai/mistral-7b-instruct:free"  # Free model

@app.post("/chat")
async def chatbot(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

        # Debug print
        print("OpenRouter Response:", response.text)

        ai_reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": ai_reply}

    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": "Something went wrong on the server. Check the logs."}
