from fastapi import FastAPI
from app.routers import dna, health, stats
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mutant DNA Analyzer API", version="1.0")

app.include_router(dna.router)
app.include_router(health.router)
app.include_router(stats.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Mutant DNA Analyzer API"}
