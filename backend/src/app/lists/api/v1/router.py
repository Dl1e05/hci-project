from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.core.security import get_user_from_token
from app.lists.models import WatchStatus
from app.lists.schemas import (
    UserContentListCreate,
    UserContentListUpdate,
    WatchStatusEnum,
    UserContentListRead,
    UserContentListReadStats,
    UserContentListReadGroups,
)
from app.lists.services.services import WatchListService

router = APIRouter(prefix='/lists')

@router.post('/add/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def add_to_watchlist(
    content_id: UUID,
    data: UserContentListCreate,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Добавить контент в список"""
    try:
        entry = await WatchListService.add_to_list(
            db=db,
            user_id=current_user,
            content_id=content_id,
            data=data
        )
        return entry
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def get_watchlist_entry(
    content_id: UUID,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить запись"""
    entry = await WatchListService.get_user_list(
        db=db,
        user_id=current_user,
        content_id=content_id
    )
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return entry


@router.patch('/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def update_watchlist_entry(
    content_id: UUID,
    data: UserContentListUpdate,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить запись"""
    entry = await WatchListService.update_list_entry(
        db=db,
        user_id=current_user,
        content_id=content_id,
        data=data
    )
    if not entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return entry


@router.delete('/{content_id}', tags=['Watchlist'])
async def remove_from_watchlist(
    content_id: UUID,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить из списка"""
    success = await WatchListService.remove_from_list(
        db=db,
        user_id=current_user,
        content_id=content_id
    )
    if not success:
        raise HTTPException(status_code=404, detail='Entry not found')
    return {'message': 'Removed from watchlist'}


@router.get('/status/completed', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_completed(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить завершённые"""
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.COMPLETED,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/planned', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_planned(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить планируемые"""
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.PLANNED,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/dropped', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_dropped(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить заброшенные"""
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.DROPPED,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/all/grouped', response_model=UserContentListReadGroups, tags=['Watchlist'])
async def get_all_grouped(
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить все, сгруппированные"""
    grouped = await WatchListService.get_user_lists_grouped(
        db=db,
        user_id=current_user
    )
    return UserContentListReadGroups(**grouped)


@router.get('/stats', response_model=UserContentListReadStats, tags=['Watchlist'])
async def get_user_stats(
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить статистику"""
    stats = await WatchListService.get_user_stats(
        db=db,
        user_id=current_user
    )
    return UserContentListReadStats(**stats)


@router.post('/{content_id}/mark-completed', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_completed(
    content_id: UUID,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Отметить как завершено"""
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        data = UserContentListCreate(status=WatchStatusEnum.COMPLETED)
        entry = await WatchListService.add_to_list(db, current_user, content_id, data)
    else:
        data = UserContentListUpdate(status=WatchStatusEnum.COMPLETED)
        entry = await WatchListService.update_list_entry(db, current_user, content_id, data)
    return entry


@router.post('/{content_id}/mark-planned', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_planned(
    content_id: UUID,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Отметить как планирую"""
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        data = UserContentListCreate(status=WatchStatusEnum.PLANNED)
        entry = await WatchListService.add_to_list(db, current_user, content_id, data)
    else:
        data = UserContentListUpdate(status=WatchStatusEnum.PLANNED)
        entry = await WatchListService.update_list_entry(db, current_user, content_id, data)
    return entry


@router.post('/{content_id}/mark-dropped', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_dropped(
    content_id: UUID,
    current_user: UUID = Depends(get_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """Отметить как забросил"""
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        data = UserContentListCreate(status=WatchStatusEnum.DROPPED)
        entry = await WatchListService.add_to_list(db, current_user, content_id, data)
    else:
        data = UserContentListUpdate(status=WatchStatusEnum.DROPPED)
        entry = await WatchListService.update_list_entry(db, current_user, content_id, data)
    return entry