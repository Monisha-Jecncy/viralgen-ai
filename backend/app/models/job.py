from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class StyleType(str, Enum):
    LUXURY = "luxury"
    MODERN = "modern"
    MINIMAL = "minimal"
    FUNNY = "funny"
    PROFESSIONAL = "professional"


class GenerateRequest(BaseModel):
    prompt: str
    style: StyleType = StyleType.PROFESSIONAL


class GenerateResponse(BaseModel):
    success: bool
    job_id: Optional[str] = None
    image_url: Optional[str] = None
    marketing_copy: Optional[str] = None
    enhanced_prompt: Optional[str] = None
    error: Optional[str] = None
    status: str = "pending"


class JobStatus(BaseModel):
    job_id: str
    status: str
    image_url: Optional[str] = None
    marketing_copy: Optional[str] = None
    enhanced_prompt: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
