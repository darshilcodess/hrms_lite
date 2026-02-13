from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import attendance as attendance_service
from app.schemas.attendance import AttendanceCreate, AttendanceResponse

router = APIRouter()


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
):
    return attendance_service.create_attendance(db, payload)


@router.get("", response_model=list[AttendanceResponse])
def get_attendance(employee_id: int, db: Session = Depends(get_db)):
    return attendance_service.get_attendance_by_employee(db, employee_id)
