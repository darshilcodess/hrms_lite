"""Seed database with sample employees and attendance.

Matches models: Employee (employee_id, full_name, email, department),
               Attendance (employee_id FK, date, status: Present|Absent).

Run from server/: python -m app.utils.seed_data
"""

from datetime import date

from app.core.database import SessionLocal
from app.models.employee import Employee
from app.models.attendance import Attendance


# Employee model fields (id, created_at are auto)
SEED_EMPLOYEES = [
    {"employee_id": "E001", "full_name": "Alice Johnson", "email": "alice.johnson@company.com", "department": "Engineering"},
    {"employee_id": "E002", "full_name": "Bob Smith", "email": "bob.smith@company.com", "department": "Product"},
    {"employee_id": "E003", "full_name": "Carol Williams", "email": "carol.williams@company.com", "department": "Design"},
    {"employee_id": "E004", "full_name": "David Brown", "email": "david.brown@company.com", "department": "Engineering"},
    {"employee_id": "E005", "full_name": "Eva Davis", "email": "eva.davis@company.com", "department": "HR"},
]

# Attendance: employee_id is looked up by employee_id string; date and status match model
# status must be "Present" or "Absent" (Enum)
SEED_ATTENDANCE = [
    ("E001", date(2025, 2, 10), "Present"),
    ("E001", date(2025, 2, 11), "Absent"),
    ("E001", date(2025, 2, 12), "Present"),
    ("E002", date(2025, 2, 10), "Present"),
    ("E002", date(2025, 2, 11), "Present"),
    ("E003", date(2025, 2, 10), "Present"),
    ("E003", date(2025, 2, 11), "Absent"),
    ("E004", date(2025, 2, 10), "Absent"),
    ("E004", date(2025, 2, 12), "Present"),
    ("E005", date(2025, 2, 10), "Present"),
]


def seed_employees(db) -> None:
    for data in SEED_EMPLOYEES:
        existing = db.query(Employee).filter(
            (Employee.employee_id == data["employee_id"]) | (Employee.email == data["email"])
        ).first()
        if not existing:
            db.add(Employee(**data))


def seed_attendance(db) -> None:
    for employee_code, att_date, status in SEED_ATTENDANCE:
        employee = db.query(Employee).filter(Employee.employee_id == employee_code).first()
        if not employee:
            continue
        existing = db.query(Attendance).filter(
            Attendance.employee_id == employee.id,
            Attendance.date == att_date,
        ).first()
        if existing:
            continue
        db.add(Attendance(employee_id=employee.id, date=att_date, status=status))


def run_seed() -> None:
    db = SessionLocal()
    try:
        seed_employees(db)
        db.commit()
        seed_attendance(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
    print("Seed complete: employees and attendance created if missing.")
