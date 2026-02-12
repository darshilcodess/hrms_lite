from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    existing = db.query(Employee).filter(Employee.employee_id == employee_data.employee_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Employee with this employee_id already exists")
    existing = db.query(Employee).filter(Employee.email == employee_data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Employee with this email already exists")

    employee = Employee(
        employee_id=employee_data.employee_id,
        full_name=employee_data.full_name,
        email=employee_data.email,
        department=employee_data.department,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_all_employees(db: Session) -> list[Employee]:
    return db.query(Employee).all()


def delete_employee(db: Session, employee_id: int) -> None:
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
