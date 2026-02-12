from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.employee import Employee
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate


def create_attendance(db: Session, attendance_data: AttendanceCreate) -> Attendance:
    employee = db.query(Employee).filter(Employee.id == attendance_data.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.employee_id == attendance_data.employee_id,
            Attendance.date == attendance_data.date,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Attendance already recorded for this employee on this date",
        )

    attendance = Attendance(
        employee_id=attendance_data.employee_id,
        date=attendance_data.date,
        status=attendance_data.status,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance


def get_attendance_by_employee(db: Session, employee_id: int) -> list[Attendance]:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return (
        db.query(Attendance)
        .filter(Attendance.employee_id == employee_id)
        .order_by(Attendance.date.desc())
        .all()
    )
