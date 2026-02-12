"""Seed database with sample employees and attendance.

Run from server/: python -m app.utils.seed_data
"""

from datetime import date

from app.core.database import SessionLocal
from app.models.employee import Employee
from app.models.attendance import Attendance


SEED_EMPLOYEES = [
    {
        "employee_id": "E001",
        "full_name": "Alice Johnson",
        "email": "alice.johnson@company.com",
        "department": "Engineering",
    },
    {
        "employee_id": "E002",
        "full_name": "Bob Smith",
        "email": "bob.smith@company.com",
        "department": "Product",
    },
    {
        "employee_id": "E003",
        "full_name": "Carol Williams",
        "email": "carol.williams@company.com",
        "department": "Design",
    },
    {
        "employee_id": "E004",
        "full_name": "David Brown",
        "email": "david.brown@company.com",
        "department": "Engineering",
    },
    {
        "employee_id": "E005",
        "full_name": "Eva Davis",
        "email": "eva.davis@company.com",
        "department": "HR",
    },
]


SEED_ATTENDANCE = [
    {"employee_code": "E001", "date": date(2025, 2, 10), "status": "Present"},
    {"employee_code": "E001", "date": date(2025, 2, 11), "status": "Absent"},
    {"employee_code": "E002", "date": date(2025, 2, 10), "status": "Present"},
    {"employee_code": "E003", "date": date(2025, 2, 10), "status": "Present"},
    {"employee_code": "E004", "date": date(2025, 2, 10), "status": "Absent"},
]


def seed_employees() -> None:
    db = SessionLocal()
    try:
        for data in SEED_EMPLOYEES:
            existing = db.query(Employee).filter(
                (Employee.employee_id == data["employee_id"])
                | (Employee.email == data["email"])
            ).first()
            if not existing:
                db.add(Employee(**data))
        db.commit()
    finally:
        db.close()


def seed_attendance() -> None:
    db = SessionLocal()
    try:
        for record in SEED_ATTENDANCE:
            employee = (
                db.query(Employee)
                .filter(Employee.employee_id == record["employee_code"])
                .first()
            )
            if not employee:
                # Skip if employee from seed list is missing
                continue

            exists = (
                db.query(Attendance)
                .filter(
                    Attendance.employee_id == employee.id,
                    Attendance.date == record["date"],
                )
                .first()
            )
            if exists:
                continue

            db.add(
                Attendance(
                    employee_id=employee.id,
                    date=record["date"],
                    status=record["status"],
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_employees()
    seed_attendance()
    print("Seed complete: employees and attendance records created if missing.")

