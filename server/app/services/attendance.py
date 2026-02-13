from datetime import date as date_type

from sqlalchemy import func
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


def get_recent_attendance_with_employee(db: Session, limit: int = 10) -> list[tuple]:
    """Return recent attendance rows with (Attendance, employee full_name)."""
    rows = (
        db.query(Attendance, Employee.full_name)
        .join(Employee, Attendance.employee_id == Employee.id)
        .order_by(Attendance.date.desc(), Attendance.id.desc())
        .limit(limit)
        .all()
    )
    return rows


def get_today_stats(db: Session, today: date_type | None = None) -> tuple[int, int]:
    """Return (present_count, absent_count) for the given date (default today)."""
    if today is None:
        today = date_type.today()
    present = (
        db.query(func.count(Attendance.id))
        .filter(Attendance.date == today, Attendance.status == "Present")
        .scalar()
        or 0
    )
    absent = (
        db.query(func.count(Attendance.id))
        .filter(Attendance.date == today, Attendance.status == "Absent")
        .scalar()
        or 0
    )
    return (present, absent)
