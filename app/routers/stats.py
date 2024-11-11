from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.db_models import DNARecord

router = APIRouter()


@router.get("/stats", response_model=dict)
async def get_stats(db: Session = Depends(get_db)):
    """
    Get the statistics of the DNA records

    Args:
    db (sqlalchemy.orm.session.Session): Database session

    Returns:
    dict: A dictionary containing the following statistics:
        - 'count_mutant_dna' (int): The number of mutant DNA records.
        - 'count_human_dna' (int): The number of human DNA records.
        - 'ratio' (float, optional): The ratio of mutants to humans (mutants/humans).
          If no human DNA records exist, the ratio is None.

    Raises:
    HTTPException: If there's an error during the database query.
    """
    try:
        total_mutants = db.query(DNARecord).filter(DNARecord.is_mutant == True).count()
        total_humans = db.query(DNARecord).filter(DNARecord.is_mutant == False).count()

        return {
            "count_mutant_dna": total_mutants,
            "count_human_dna": total_humans,
            "ratio": total_mutants / total_humans if total_humans > 0 else None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while getting stats: {str(e)}"
        )
