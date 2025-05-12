from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import zipfile
import os
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct:free"

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
        print("OpenRouter Response:", response.text)

        ai_reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": ai_reply}

    except Exception as e:
        print("❌ Error:", str(e))
        return {"error": "Something went wrong on the server. Check the logs."}

@app.post("/analyze-zip")
async def analyze_zip(file: UploadFile = File(...)):
    if file is None:
        return JSONResponse(status_code=400, content={"error": "No file received."})

    print("🧾 Received file name:", file.filename)
    print("🧾 Content type:", file.content_type)

    if not file.filename.endswith('.zip'):
        return JSONResponse(status_code=400, content={"error": "Only ZIP files are supported."})

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, file.filename)

        with open(zip_path, "wb") as f:
            f.write(await file.read())

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
        except zipfile.BadZipFile:
            return JSONResponse(status_code=400, content={"error": "Invalid ZIP file"})

        extracted_files = []
        results = []

        for root, _, files in os.walk(tmpdir):
            for fname in files:
                if fname != file.filename and fname.endswith(('.txt', '.py', '.js', '.md')):
                    full_path = os.path.join(root, fname)
                    extracted_files.append(fname)

                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as txt:
                            content = txt.read()
                            if len(content.strip()) == 0:
                                continue
                            if len(content) > 10000:
                                content = content[:10000] + "\n...(truncated)"

                            headers = {
                                "Authorization": f"Bearer {API_KEY}",
                                "Content-Type": "application/json"
                            }

                            payload = {
                                "model": MODEL,
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": f"Analyze the following file `{fname}` and summarize what it does:\n\n{content}"
                                    }
                                ]
                            }

                            ai_response = requests.post(
                                "https://openrouter.ai/api/v1/chat/completions",
                                headers=headers,
                                json=payload
                            )

                            print("AI Response for", fname, ":", ai_response.text)

                            if ai_response.status_code == 200:
                                result_text = ai_response.json()["choices"][0]["message"]["content"]
                                results.append({fname: result_text})
                            else:
                                results.append({fname: f"❌ Failed to analyze. Status: {ai_response.status_code}, Body: {ai_response.text}"})

                    except Exception as e:
                        results.append({fname: f"⚠️ Error reading file: {str(e)}"})

        print("✅ Extracted files:", extracted_files)
        print("🧠 Analysis Results:", results)

        return {
            "message": "✅ ZIP processed successfully",
            "extracted_files": extracted_files,
            "analysis": results
        }
