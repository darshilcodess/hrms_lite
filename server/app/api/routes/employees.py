from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import employee as crud_employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
):
    return crud_employee.create_employee(db, payload)


@router.get("", response_model=list[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    return crud_employee.get_all_employees(db)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_employee(id: int, db: Session = Depends(get_db)):
    crud_employee.delete_employee(db, id)
    return {"message": "Employee deleted successfully"}
