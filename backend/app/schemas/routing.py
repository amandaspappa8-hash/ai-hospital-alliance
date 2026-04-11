from pydantic import BaseModel, Field
from typing import List, Optional


class VitalsInput(BaseModel):
    bp: Optional[str] = None
    hr: Optional[int] = None
    spo2: Optional[int] = None
    temp: Optional[float] = None


class ClinicalRouteRequest(BaseModel):
    chief_complaint: str
    symptoms: List[str] = Field(default_factory=list)
    age: Optional[int] = None
    gender: Optional[str] = None
    vitals: Optional[VitalsInput] = None


class SuggestedOrder(BaseModel):
    name: str
    priority: str
    category: str


class ClinicalRouteResponse(BaseModel):
    chief_complaint: str
    triage_level: str
    urgency_score: int
    route_to: List[str]
    suggested_orders: List[SuggestedOrder]
    red_flags: List[str]
    next_actions: List[str]
    rationale: List[str]
