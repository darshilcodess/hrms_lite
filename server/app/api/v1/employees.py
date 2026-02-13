from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services import employee as employee_service
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter()


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return employee_service.create_employee(db, payload)


@router.get("", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    return employee_service.get_all_employees(db)


@router.get("/{id}", response_model=EmployeeResponse)
def get_employee(id: int, db: Session = Depends(get_db)):
    employee = employee_service.get_employee_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee_service.delete_employee(db, id)
    return {"message": "Employee deleted successfully"}
