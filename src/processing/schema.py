"""
Schema definitions for the tender extraction system.
"""
from pydantic import BaseModel
from typing import List, Optional

class TenderFilterResult(BaseModel):
    """Schema for tender filter results."""
    tender_ids: List[str]
    message: Optional[str] = None

class TenderData(BaseModel):
    """Schema for tender data."""
    tender_id: str
    title: str
    description: str
    category: str
    is_consulting: bool = False

    class Config:
        from_attributes = True