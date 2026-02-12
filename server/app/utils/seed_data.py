"""Seed database with sample employees. Run from server/: python -m app.utils.seed_data"""

from app.core.database import SessionLocal
from app.models.employee import Employee

SEED_EMPLOYEES = [
    {"employee_id": "E001", "full_name": "Alice Johnson", "email": "alice.johnson@company.com", "department": "Engineering"},
    {"employee_id": "E002", "full_name": "Bob Smith", "email": "bob.smith@company.com", "department": "Product"},
    {"employee_id": "E003", "full_name": "Carol Williams", "email": "carol.williams@company.com", "department": "Design"},
    {"employee_id": "E004", "full_name": "David Brown", "email": "david.brown@company.com", "department": "Engineering"},
    {"employee_id": "E005", "full_name": "Eva Davis", "email": "eva.davis@company.com", "department": "HR"},
]


def seed_employees():
    db = SessionLocal()
    try:
        for data in SEED_EMPLOYEES:
            existing = db.query(Employee).filter(
                (Employee.employee_id == data["employee_id"]) | (Employee.email == data["email"])
            ).first()
            if not existing:
                db.add(Employee(**data))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_employees()
    print("Seed complete: 5 employee records.")
