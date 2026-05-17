from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import search
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TFG AI Matchmaker API")

# El CORS se configura SOLO aquí una vez
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos las rutas de search.py
app.include_router(search.router, prefix="/api/v1", tags=["Matchmaking"])

@app.get("/")
async def root():
    return {"message": "API Online", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)