"""
Modelo base para todos os modelos do CERBERUS.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel as PydanticBaseModel, ConfigDict


class BaseModel(PydanticBaseModel):
    """Modelo base com configurações comuns."""
    
    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
    )
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.now()
