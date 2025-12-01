from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.lists.models import UserContentList, WatchStatus
from app.lists.schemas import VALID_STATUS_COMBINATIONS, UserContentListCreate, UserContentListUpdate


class WatchListService:
    @staticmethod
    async def add_to_list(db: AsyncSession, user_id: UUID, content_id: UUID, data: UserContentListCreate) -> UserContentList:
        existing = await db.execute(
            select(UserContentList).where(UserContentList.user_id == user_id, UserContentList.content_id == content_id)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Content already in user's list.")

        entry = UserContentList(
            user_id=user_id,
            content_id=content_id,
            content_type=data.content_type,
            status=data.status,
        )

        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def get_user_list(db: AsyncSession, user_id: UUID, content_id: UUID) -> UserContentList | None:
        result = await db.execute(
            select(UserContentList).where(UserContentList.user_id == user_id, UserContentList.content_id == content_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_list_entry(
        db: AsyncSession, user_id: UUID, content_id: UUID, data: UserContentListUpdate
    ) -> UserContentList | None:
        entry = await WatchListService.get_user_list(db, user_id, content_id)
        if not entry:
            return None

        if data.status is not None:
            if data.status not in VALID_STATUS_COMBINATIONS.get(entry.content_type, set()):
                raise HTTPException(
                    status_code=400,
                    detail=f"Status '{data.status.value}' is not valid for content type '{entry.content_type.value}'",
                )
            entry.status = data.status

        await db.commit()
        await db.refresh(entry)
        return entry

    @staticmethod
    async def remove_from_list(db: AsyncSession, user_id: UUID, content_id: UUID) -> bool:
        entry = await WatchListService.get_user_list(db, user_id, content_id)
        if not entry:
            return False

        await db.delete(entry)
        await db.commit()
        return True

    @staticmethod
    async def get_user_list_by_status(
        db: AsyncSession, user_id: UUID, status: WatchStatus, skip: int = 0, limit: int = 20
    ) -> tuple[list[UserContentList], int]:
        count_result = await db.execute(
            select(func.count(UserContentList.id)).where(UserContentList.user_id == user_id, UserContentList.status == status)
        )
        total = count_result.scalar() or 0

        result = await db.execute(
            select(UserContentList)
            .where(UserContentList.user_id == user_id, UserContentList.status == status)
            .order_by(desc(UserContentList.id))
            .offset(skip)
            .limit(limit)
        )
        entries = result.scalars().all()
        return list(entries), total

    @staticmethod
    async def get_user_lists_grouped(db: AsyncSession, user_id: UUID) -> dict[str, list[UserContentList]]:
        result = await db.execute(
            select(UserContentList).where(UserContentList.user_id == user_id).order_by(desc(UserContentList.id))
        )
        entries = result.scalars().all()

        grouped: dict[str, list[UserContentList]] = {
            'completed': [],
            'planned': [],
            'dropped': [],
            'watching': [],
            'postponed': [],
            'read': [],
            'reading': [],
            'finished': [],
            'playing': [],
        }

        for entry in entries:
            grouped[entry.status.value].append(entry)

        return grouped

    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: UUID) -> dict:
        result = await db.execute(
            select(UserContentList.status, func.count(UserContentList.id).label('count'))
            .where(UserContentList.user_id == user_id)
            .group_by(UserContentList.status)
        )

        stats = result.fetchall()

        counts = {
            'completed_count': 0,
            'planned_count': 0,
            'dropped_count': 0,
            'watching_count': 0,
            'postponed_count': 0,
            'read_count': 0,
            'reading_count': 0,
            'finished_count': 0,
            'playing_count': 0,
        }

        for status, count in stats:
            if status == WatchStatus.COMPLETED:
                counts['completed_count'] = count
            elif status == WatchStatus.PLANNED:
                counts['planned_count'] = count
            elif status == WatchStatus.DROPPED:
                counts['dropped_count'] = count
            elif status == WatchStatus.WATCHING:
                counts['watching_count'] = count
            elif status == WatchStatus.POSTPONED:
                counts['postponed_count'] = count
            elif status == WatchStatus.READ:
                counts['read_count'] = count
            elif status == WatchStatus.READING:
                counts['reading_count'] = count
            elif status == WatchStatus.FINISHED:
                counts['finished_count'] = count
            elif status == WatchStatus.PLAYING:
                counts['playing_count'] = count

        return counts
