from fastapi import FastAPI
from app.routers import dna, health

app = FastAPI(title="Mutant DNA Analyzer API", version="1.0")

app.include_router(dna.router)
app.include_router(health.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Mutant DNA Analyzer API"}
