from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.base import BaseContent
from app.core.db import get_async_session
from app.core.deps import require_user_from_cookie
from app.lists.models import ContentType, UserContentList, WatchStatus
from app.lists.schemas import (
    UserContentListCreate,
    UserContentListRead,
    UserContentListReadGroups,
    UserContentListReadStats,
    UserContentListUpdate,
)
from app.lists.services.services import WatchListService

router = APIRouter(prefix='/lists')


async def _get_content_type_from_db(db: AsyncSession, content_id: UUID) -> ContentType:
    """Helper to determine content_type from content_id by querying the contents table."""
    result = await db.execute(select(BaseContent.content_type).where(BaseContent.id == content_id))
    content_type_str = result.scalar_one_or_none()
    if not content_type_str:
        raise HTTPException(status_code=404, detail='Content not found')

    if content_type_str in ('film', 'series', 'anime', 'video'):
        return ContentType.MEDIA
    if content_type_str == 'game':
        return ContentType.GAMES
    if content_type_str in ('book', 'article', 'course', 'podcast'):
        return ContentType.LITERATURE
    raise HTTPException(status_code=400, detail=f'Unknown content type: {content_type_str}')


@router.get('/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def get_watchlist_entry(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db=db, user_id=current_user, content_id=content_id)
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return entry


@router.patch('/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def update_watchlist_entry(
    content_id: UUID, request: Request, data: UserContentListUpdate, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.update_list_entry(db=db, user_id=current_user, content_id=content_id, data=data)
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return entry


@router.delete('/{content_id}', tags=['Watchlist'])
async def remove_from_watchlist(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> dict[str, str]:
    current_user = require_user_from_cookie(request)
    success = await WatchListService.remove_from_list(db=db, user_id=current_user, content_id=content_id)
    if not success:
        raise HTTPException(status_code=404, detail='Entry not found')
    return {'message': 'Removed from watchlist'}


@router.get('/all/grouped', response_model=UserContentListReadGroups, tags=['Watchlist'])
async def get_all_grouped(request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentListReadGroups:
    current_user = require_user_from_cookie(request)
    grouped = await WatchListService.get_user_lists_grouped(db=db, user_id=current_user)
    return UserContentListReadGroups(**grouped)


@router.get('/stats', response_model=UserContentListReadStats, tags=['Watchlist'])
async def get_user_stats(request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentListReadStats:
    current_user = require_user_from_cookie(request)
    stats = await WatchListService.get_user_stats(db=db, user_id=current_user)
    return UserContentListReadStats(**stats)


@router.post('/{content_id}/mark-completed', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_completed(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        content_type = await _get_content_type_from_db(db, content_id)
        create_data = UserContentListCreate(content_type=content_type, status=WatchStatus.COMPLETED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatus.COMPLETED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-planned', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_planned(content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        content_type = await _get_content_type_from_db(db, content_id)
        create_data = UserContentListCreate(content_type=content_type, status=WatchStatus.PLANNED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatus.PLANNED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-dropped', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_dropped(content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        content_type = await _get_content_type_from_db(db, content_id)
        create_data = UserContentListCreate(content_type=content_type, status=WatchStatus.DROPPED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatus.DROPPED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-watching', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_watching(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        content_type = await _get_content_type_from_db(db, content_id)
        create_data = UserContentListCreate(content_type=content_type, status=WatchStatus.WATCHING)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatus.WATCHING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-postponed', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_postponed(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        content_type = await _get_content_type_from_db(db, content_id)
        create_data = UserContentListCreate(content_type=content_type, status=WatchStatus.POSTPONED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatus.POSTPONED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-read', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_read(content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatus.READ)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-reading', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_reading(content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatus.READING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-finished', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_finished(
    content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatus.FINISHED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-playing', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_playing(content_id: UUID, request: Request, db: AsyncSession = Depends(get_async_session)) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatus.PLAYING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry
