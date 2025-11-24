from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.deps import require_user_from_cookie
from app.lists.models import UserContentList, WatchStatus
from app.lists.schemas import (
    UserContentListCreate,
    UserContentListRead,
    UserContentListReadGroups,
    UserContentListReadStats,
    UserContentListUpdate,
    WatchStatusEnum,
)
from app.lists.services.services import WatchListService

router = APIRouter(prefix='/lists')

@router.post('/add/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def add_to_watchlist(
    content_id: UUID,
    request: Request,
    data: UserContentListCreate,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    try:
        return await WatchListService.add_to_list(
            db=db,
            user_id=current_user,
            content_id=content_id,
            data=data
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get('/{content_id}', response_model=UserContentListRead, tags=['Watchlist'])
async def get_watchlist_entry(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
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
    request: Request,
    data: UserContentListUpdate,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
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
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> dict[str, str]:
    current_user = require_user_from_cookie(request)
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
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
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
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
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
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.DROPPED,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/watching', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_watching(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.WATCHING,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/postponed', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_postponed(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.POSTPONED,
        skip=skip,
        limit=limit
    )
    return entries

@router.get('/status/read', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_read(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.READ,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/reading', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_reading(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.READING,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/finished', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_finished(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.FINISHED,
        skip=skip,
        limit=limit
    )
    return entries


@router.get('/status/playing', response_model=list[UserContentListRead], tags=['Watchlist'])
async def get_playing(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
) -> list[UserContentList]:
    current_user = require_user_from_cookie(request)
    entries, _ = await WatchListService.get_user_list_by_status(
        db=db,
        user_id=current_user,
        status=WatchStatus.PLAYING,
        skip=skip,
        limit=limit
    )
    return entries

@router.get('/all/grouped', response_model=UserContentListReadGroups, tags=['Watchlist'])
async def get_all_grouped(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentListReadGroups:
    current_user = require_user_from_cookie(request)
    grouped = await WatchListService.get_user_lists_grouped(
        db=db,
        user_id=current_user
    )
    return UserContentListReadGroups(**grouped)


@router.get('/stats', response_model=UserContentListReadStats, tags=['Watchlist'])
async def get_user_stats(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentListReadStats:
    current_user = require_user_from_cookie(request)
    stats = await WatchListService.get_user_stats(
        db=db,
        user_id=current_user
    )
    return UserContentListReadStats(**stats)


@router.post('/{content_id}/mark-completed', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_completed(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        create_data = UserContentListCreate(status=WatchStatusEnum.COMPLETED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatusEnum.COMPLETED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-planned', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_planned(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        create_data = UserContentListCreate(status=WatchStatusEnum.PLANNED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatusEnum.PLANNED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-dropped', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_dropped(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        create_data = UserContentListCreate(status=WatchStatusEnum.DROPPED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatusEnum.DROPPED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-watching', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_watching(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        create_data = UserContentListCreate(status=WatchStatusEnum.WATCHING)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatusEnum.WATCHING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-postponed', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_postponed(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        create_data = UserContentListCreate(status=WatchStatusEnum.POSTPONED)
        return await WatchListService.add_to_list(db, current_user, content_id, create_data)
    update_data = UserContentListUpdate(status=WatchStatusEnum.POSTPONED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry

@router.post('/{content_id}/mark-read', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_read(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatusEnum.READ)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-reading', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_reading(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatusEnum.READING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-finished', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_finished(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatusEnum.FINISHED)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry


@router.post('/{content_id}/mark-playing', response_model=UserContentListRead, tags=['Watchlist'])
async def mark_as_playing(
    content_id: UUID,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
) -> UserContentList:
    current_user = require_user_from_cookie(request)
    entry = await WatchListService.get_user_list(db, current_user, content_id)
    if not entry:
        raise HTTPException(status_code=400, detail='Content not in list. Use /add endpoint first.')
    update_data = UserContentListUpdate(status=WatchStatusEnum.PLAYING)
    updated_entry = await WatchListService.update_list_entry(db, current_user, content_id, update_data)
    if not updated_entry:
        raise HTTPException(status_code=404, detail='Entry not found')
    return updated_entry
