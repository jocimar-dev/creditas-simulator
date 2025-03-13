from pydantic import BaseModel
from typing import Optional

class PersonalRequest(BaseModel):
    full_name: str
    document_number: str
    marital_status: str
    dependents: Optional[int] = 0
