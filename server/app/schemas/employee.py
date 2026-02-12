from datetime import datetime

from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    employee_id: str
    full_name: str
    email: EmailStr
    department: str


class EmployeeResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    employee_id: str
    full_name: str
    email: str
    department: str
    created_at: datetime
