from fastapi import FastAPI, HTTPException
from agents.orchestrator import analyze_tradition
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite
        "http://localhost:3000",   # CRA (safe to keep)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"status": "IKS Backend Running"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "agents": ["knowledge", "career", "learning", "cultural"]
    }

@app.post("/api/tradition/analyze")
async def analyze(data: dict):
    tradition = data.get("tradition")
    query = data.get("query", "")

    if not tradition:
        raise HTTPException(400, "tradition field is required")

    return await analyze_tradition(tradition, query)
