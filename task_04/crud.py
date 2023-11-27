from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload, selectinload

from config import DB_URL
from models import Department, Employee, Base


def create_department(
    session: Session,
    name: str,
    address: str,
) -> Department:
    department = Department(
        name=name,
        address=address,
    )
    session.add(department)
    session.commit()
    return department


def create_employees(
    session: Session,
    *full_names: str,
    department: Department,
) -> list[Employee]:
    employees = [
        Employee(
            full_name=full_name,
            department=department,
        )
        for full_name in full_names
    ]
    session.add_all(employees)
    session.commit()
    return employees


def fetch_departments(session: Session):
    # return session.query(Department).all()
    return session.query(Department).order_by(Department.id).all()


def fetch_employees_with_departments(session: Session):
    return (
        session
        # fetch users
        .query(Employee)
        # extra options for SQLA
        .options(
            # join for each row
            # joinedload(Employee.department),
            selectinload(Employee.department),
        )
        .order_by(Employee.id)
        .all()
    )


def main():
    engine = create_engine(
        url=DB_URL,
        # echo=False,
        echo=True,
    )
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    with Session(bind=engine) as session:
        sales_dep = create_department(
            session=session,
            name="Sales",
            address="Sa st, Le b.",
        )
        it_dep = create_department(
            session=session,
            name="IT",
            address="Go st, gle b.",
        )

        create_employees(
            session,
            "Kate White",
            "Lana Green",
            "Jane March",
            department=sales_dep,
        )
        create_employees(
            session,
            "John Smith",
            "Kyle Black",
            "Sam Brown",
            department=it_dep,
        )

        fetch_departments(session)
        fetch_employees_with_departments(session)


if __name__ == "__main__":
    main()
