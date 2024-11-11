from fastapi import APIRouter, HTTPException, Depends
from app.models.dna import DNASequence
from app.services.dna_analyzer import MutantDNA

from app.models.db_models import DNARecord
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.post("/mutant", response_model=dict)
async def check_mutant(dna_sequence: DNASequence, db: Session = Depends(get_db)):
    """
    Checks if the given DNA sequence belongs to a mutant or not.

    This endpoint receives a DNA sequence, verifies if the sequence already exists in the 
    database, and if not, analyzes the sequence to determine if it corresponds to a mutant. 
    If the DNA sequence belongs to a mutant, a message confirming this is returned. If it's a human DNA,
    a 403 Forbidden response with a message is returned.

    Args:
    dna_sequence (DNASequence): The DNA sequence to be checked.
    db (Session): The SQLAlchemy database session used to query the database.

    Returns:
    dict: A dictionary containing a message stating whether the DNA is mutant or not.
    
    Raises:
    HTTPException: If an error occurs during database operations or the analysis.
    """
    try:
        dna_str = "".join(dna_sequence.dna)
        record = db.query(DNARecord).filter(DNARecord.sequence == dna_str).first()

        if record:
            if record.is_mutant:
                return {"message": "DNA is mutant"}
            raise HTTPException(status_code=403, detail="DNA is not mutant")

        analyzer = MutantDNA(dna_sequence.dna)
        is_mutant = analyzer.is_mutant()
        new_record = DNARecord(sequence=dna_str, is_mutant=is_mutant)
        db.add(new_record)
        db.commit()

        if is_mutant:
            return {"message": "DNA is mutant"}
        raise HTTPException(status_code=403, detail="DNA is not mutant")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while checking mutant: {str(e)}"
        )
