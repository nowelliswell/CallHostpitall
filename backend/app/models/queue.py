from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PatientBase(BaseModel):
    name: str = Field(..., min_length=2, description="Patient name")
    poly: str = Field(..., description="Poly/Department")

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: Optional[int] = None
    number: int = Field(..., description="Queue number")
    created_at: datetime = Field(default_factory=datetime.now)
    called_at: Optional[datetime] = None

class QueueStatus(BaseModel):
    poly: str
    current_queue: List[Patient]
    called_patients: List[Patient]
    current_number: int
    total_waiting: int

class QueueResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class CallPatientRequest(BaseModel):
    poly: str

class RecallPatientRequest(BaseModel):
    patient_id: int
    poly: str