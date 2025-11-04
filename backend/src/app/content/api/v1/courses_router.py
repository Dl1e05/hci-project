from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.content.schemas.content import CourseRead, CourseUpdate
from app.content.schemas.forms import CourseFormData
from app.content.services.course_service import CourseService
from app.core.db import get_async_session
from app.core.storage import get_storage_service

router = APIRouter(prefix='/content')


@router.post('/courses', response_model=CourseRead, status_code=HTTP_201_CREATED, tags=['courses'])
async def create_course(
    form_data: CourseFormData = Depends(),
    banner: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_session),
) -> CourseRead:
    try:
        storage = get_storage_service()

        banner_key = storage.upload_file(banner.file, banner.filename or 'banner', banner.content_type, 'banners')
        banner_url = storage.get_public_url(banner_key)

        course_data = form_data.to_schema(banner_url=banner_url)

        return await CourseService.create(db, course_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@router.get('/courses', response_model=list[CourseRead], tags=['courses'])
async def get_all_courses(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)) -> list[CourseRead]:
    return await CourseService.get_all(db, skip=skip, limit=limit)


@router.get('/courses/{course_id}', response_model=CourseRead, tags=['courses'])
async def get_course(course_id: UUID, db: AsyncSession = Depends(get_async_session)) -> CourseRead:
    course = await CourseService.get_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with id {course_id} not found')
    return course


@router.patch('/courses/{course_id}', response_model=CourseRead, tags=['courses'])
async def update_course(
    course_id: UUID, course_data: CourseUpdate, db: AsyncSession = Depends(get_async_session)
) -> CourseRead:
    course = await CourseService.update(db, course_id, course_data)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with id {course_id} not found')
    return course


@router.delete('/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['courses'])
async def delete_course(course_id: UUID, db: AsyncSession = Depends(get_async_session)) -> None:
    deleted = await CourseService.delete(db, course_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Course with id {course_id} not found')
