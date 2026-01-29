from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


async def create_student(
    db: AsyncSession, student: StudentCreate, user_id: UUID
) -> Student:
    db_student = Student(**student.model_dump(), user_id=user_id)
    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


async def get_students(
    db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
) -> List[Student]:
    result = await db.execute(
        select(Student).where(Student.user_id == user_id).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_student(
    db: AsyncSession, student_id: UUID, user_id: UUID
) -> Optional[Student]:
    result = await db.execute(
        select(Student).where(Student.id == student_id, Student.user_id == user_id)
    )
    return result.scalars().first()


async def update_student(
    db: AsyncSession, student_id: UUID, student: StudentUpdate, user_id: UUID
) -> Optional[Student]:
    db_student = await get_student(db, student_id, user_id)
    if not db_student:
        return None

    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.add(db_student)
    await db.commit()
    await db.refresh(db_student)
    return db_student


async def delete_student(
    db: AsyncSession, student_id: UUID, user_id: UUID
) -> Optional[Student]:
    db_student = await get_student(db, student_id, user_id)
    if not db_student:
        return None

    await db.delete(db_student)
    await db.commit()
    return db_student
