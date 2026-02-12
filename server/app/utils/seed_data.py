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
    {"employee_id": "E006", "full_name": "Frank Miller", "email": "frank.miller@company.com", "department": "Engineering"},
    {"employee_id": "E007", "full_name": "Grace Lee", "email": "grace.lee@company.com", "department": "Product"},
    {"employee_id": "E008", "full_name": "Henry Wilson", "email": "henry.wilson@company.com", "department": "Design"},
    {"employee_id": "E009", "full_name": "Ivy Chen", "email": "ivy.chen@company.com", "department": "HR"},
    {"employee_id": "E010", "full_name": "Jack Taylor", "email": "jack.taylor@company.com", "department": "Engineering"},
    {"employee_id": "E011", "full_name": "Kate Martinez", "email": "kate.martinez@company.com", "department": "Product"},
    {"employee_id": "E012", "full_name": "Leo Anderson", "email": "leo.anderson@company.com", "department": "Design"},
    {"employee_id": "E013", "full_name": "Mia Thomas", "email": "mia.thomas@company.com", "department": "Engineering"},
    {"employee_id": "E014", "full_name": "Noah Jackson", "email": "noah.jackson@company.com", "department": "HR"},
    {"employee_id": "E015", "full_name": "Olivia White", "email": "olivia.white@company.com", "department": "Product"},
    {"employee_id": "E016", "full_name": "Paul Harris", "email": "paul.harris@company.com", "department": "Design"},
    {"employee_id": "E017", "full_name": "Quinn Clark", "email": "quinn.clark@company.com", "department": "Engineering"},
    {"employee_id": "E018", "full_name": "Rachel Lewis", "email": "rachel.lewis@company.com", "department": "HR"},
    {"employee_id": "E019", "full_name": "Sam Robinson", "email": "sam.robinson@company.com", "department": "Product"},
    {"employee_id": "E020", "full_name": "Tina Walker", "email": "tina.walker@company.com", "department": "Design"},
    {"employee_id": "E021", "full_name": "Uma Hall", "email": "uma.hall@company.com", "department": "Engineering"},
    {"employee_id": "E022", "full_name": "Victor Young", "email": "victor.young@company.com", "department": "HR"},
    {"employee_id": "E023", "full_name": "Wendy King", "email": "wendy.king@company.com", "department": "Product"},
    {"employee_id": "E024", "full_name": "Xavier Wright", "email": "xavier.wright@company.com", "department": "Design"},
    {"employee_id": "E025", "full_name": "Yara Scott", "email": "yara.scott@company.com", "department": "Engineering"},
]

# Attendance: (employee_code, date, status). status must be "Present" or "Absent" (Enum)
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
    ("E006", date(2025, 2, 10), "Present"),
    ("E006", date(2025, 2, 11), "Present"),
    ("E007", date(2025, 2, 12), "Absent"),
    ("E008", date(2025, 2, 10), "Present"),
    ("E009", date(2025, 2, 11), "Present"),
    ("E010", date(2025, 2, 12), "Absent"),
    ("E011", date(2025, 2, 10), "Present"),
    ("E015", date(2025, 2, 11), "Absent"),
    ("E020", date(2025, 2, 12), "Present"),
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
