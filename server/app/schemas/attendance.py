from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    status: Literal["Present", "Absent"]


class AttendanceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    employee_id: int
    date: date
    status: str
    created_at: datetime


class AttendanceWithEmployeeResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    date: date
    status: str
