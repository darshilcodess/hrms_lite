from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import employee as employee_service
from app.services import attendance as attendance_service
from app.schemas.attendance import AttendanceWithEmployeeResponse

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return total_employees, present_today, absent_today."""
    employees = employee_service.get_all_employees(db)
    present_today, absent_today = attendance_service.get_today_stats(db)
    return {
        "total_employees": len(employees),
        "present_today": present_today,
        "absent_today": absent_today,
    }


@router.get("/recent-attendance", response_model=list[AttendanceWithEmployeeResponse])
def get_recent_attendance(limit: int = 10, db: Session = Depends(get_db)):
    """Return recent attendance records with employee names."""
    rows = attendance_service.get_recent_attendance_with_employee(db, limit=limit)
    return [
        AttendanceWithEmployeeResponse(
            id=att.id,
            employee_id=att.employee_id,
            employee_name=full_name,
            date=att.date,
            status=att.status,
        )
        for att, full_name in rows
    ]
