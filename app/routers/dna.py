from fastapi import APIRouter, HTTPException, Depends
from app.models.dna import DNASequence
from app.services.dna_analyzer import MutantDNA

router = APIRouter()

@router.post("/mutant", response_model=dict)
async def check_mutant(dna_sequence: DNASequence):
    analyzer = MutantDNA(dna_sequence.dna)
    is_mutant = analyzer.is_mutant()
    print(is_mutant)
    if is_mutant:
        return {"message": "DNA is mutant"}
    raise HTTPException(status_code=403, detail="DNA is not mutant")