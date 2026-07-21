"""
Backend pour Hugging Face Space (Docker).
Sert à la fois l'API (transcription + chat) et le frontend statique sur un seul port.

- /transcribe : audio -> texte (faster-whisper)
- /chat       : texte -> correction + réponse (Mistral GGUF via llama-cpp-python)
- /           : sert le frontend (static/index.html)
"""

import os
import tempfile

from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from faster_whisper import WhisperModel
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

app = FastAPI(title="English Practice API")

# --- Whisper (STT) ---
# "small" = compromis correct pour un CPU de Space gratuit.
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "small")
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")

# --- LLM (Mistral, quantifié GGUF, via llama-cpp-python) ---
# Modèle communautaire quantifié, léger et adapté au CPU.
LLM_REPO = os.environ.get("LLM_REPO", "TheBloke/Mistral-7B-Instruct-v0.2-GGUF")
LLM_FILE = os.environ.get("LLM_FILE", "mistral-7b-instruct-v0.2.Q4_K_M.gguf")

llm_path = hf_hub_download(repo_id=LLM_REPO, filename=LLM_FILE)
llm = Llama(
    model_path=llm_path,
    n_ctx=2048,
    n_threads=os.cpu_count(),
    verbose=False,
)

SYSTEM_PROMPT = """You are a friendly English tutor helping a French speaker practice \
listening comprehension and speaking. The user will send you a transcription of \
something they said in English (it may contain mistakes due to speech-to-text \
errors or their own English level).

Respond in this exact format:

CORRECTION: <the corrected version of their sentence, or "No errors!" if it's already correct>
EXPLANATION: <1-2 short sentences in French explaining the main error, if any>
REPLY: <a natural English reply to continue the conversation, 1-3 sentences, \
adapted to an intermediate learner>
"""


class ChatRequest(BaseModel):
    text: str


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    suffix = os.path.splitext(audio.filename or "audio.webm")[1] or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    try:
        segments, info = whisper_model.transcribe(tmp_path, language="en")
        text = " ".join(segment.text.strip() for segment in segments)
    finally:
        os.unlink(tmp_path)

    return {"text": text.strip(), "detected_language": info.language}


@app.post("/chat")
async def chat(req: ChatRequest):
    prompt = f"<s>[INST] {SYSTEM_PROMPT}\n\nUser said: \"{req.text}\" [/INST]"

    output = llm(
        prompt,
        max_tokens=300,
        temperature=0.7,
        stop=["</s>", "[INST]"],
    )
    text = output["choices"][0]["text"].strip()

    return {"raw": text}


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "whisper_model": WHISPER_MODEL_SIZE,
        "llm_repo": LLM_REPO,
        "llm_file": LLM_FILE,
    }


# Sert le frontend statique (doit être déclaré après les routes API)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")