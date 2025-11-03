from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Course
from app.content.repo import ContentRepository
from app.content.schemas.content import CourseCreate, CourseRead, CourseUpdate


class CourseService:
    @staticmethod
    async def create(db: AsyncSession, course_data: CourseCreate) -> CourseRead:
        data = course_data.model_dump()
        course = await ContentRepository.create(db, Course, data)
        return CourseRead.model_validate(course)

    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[CourseRead]:
        courses = await ContentRepository.get_all(db, Course, skip, limit)
        return [CourseRead.model_validate(course) for course in courses]

    @staticmethod
    async def get_by_id(db: AsyncSession, course_id: UUID) -> CourseRead | None:
        course = await ContentRepository.get_by_id(db, Course, course_id)
        return CourseRead.model_validate(course) if course else None

    @staticmethod
    async def update(db: AsyncSession, course_id: UUID, course_data: CourseUpdate) -> CourseRead | None:
        data = course_data.model_dump(exclude_unset=True)
        course = await ContentRepository.update(db, Course, course_id, data)
        return CourseRead.model_validate(course) if course else None

    @staticmethod
    async def delete(db: AsyncSession, course_id: UUID) -> bool:
        return await ContentRepository.delete(db, Course, course_id)

