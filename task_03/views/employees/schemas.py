from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    full_name: str
    email: EmailStr


class EmployeeCreate(EmployeeBase):
    ...


class Employee(EmployeeBase):
    id: int
