from sqlalchemy import Column, String, Boolean
from app.core.database import Base

class DNARecord(Base):
    """
    DNARecord model to store DNA sequences and their classification as mutant or human.
    """
    __tablename__ = "dna_records"
    
    sequence = Column(String, primary_key=True, unique=True, index=True)
    is_mutant = Column(Boolean, nullable=False)
    