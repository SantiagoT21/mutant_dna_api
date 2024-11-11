from typing import List
from pydantic import BaseModel


class DNASequence(BaseModel):
    dna: List[str]

    class Config:
        schema_extra = {
            "example": {
                "dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
            }
        }
