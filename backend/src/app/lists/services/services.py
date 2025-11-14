from uuid import UUID

from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.lists.models import UserContentList, WatchStatus
from app.lists.schemas import UserContentListCreate, UserContentListUpdate, WatchStatusEnum


class WatchListService:
    @staticmethod
    async def add_to_list(
        db: AsyncSession,
        user_id: UUID,
        content_id: UUID,
        data: UserContentListCreate
    ) -> UserContentList:
        existing = await db.execute(
            select(UserContentList).where(
                UserContentList.user_id == user_id,
                UserContentList.content_id == content_id
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Content already in user's list.")

        entry = UserContentList(
            user_id=user_id,
            content_id=content_id,
            status=WatchStatus(data.status.value)
        )

        db.add(entry)
        await db.commit()
        await db.refresh(entry)
        return entry
    
    @staticmethod
    async def get_user_list(
        db: AsyncSession,
        user_id: UUID,
        content_id: UUID
    ) -> UserContentList | None:
        result = await db.execute(
            select(UserContentList).where(
                UserContentList.user_id == user_id,
                UserContentList.content_id == content_id
            )
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_list_entry(
        db: AsyncSession,
        user_id: UUID,
        content_id: UUID,
        data: UserContentListUpdate
    ) -> UserContentList | None:
        entry = await WatchListService.get_user_list(db, user_id, content_id)
        if not entry:
            return None
        
        if data.status is not None:
            entry.status = WatchStatus(data.status.value)
        
        await db.commit()
        await db.refresh(entry)
        return entry
    
    @staticmethod
    async def remove_from_list(
        db: AsyncSession,
        user_id: UUID,
        content_id: UUID
    ) -> bool:
        entry = await WatchListService.get_user_list(db, user_id, content_id)
        if not entry:
            return False
        
        await db.delete(entry)
        await db.commit()
        return True
    
    @staticmethod
    async def get_user_list_by_status(
        db: AsyncSession,
        user_id: UUID,
        status: WatchStatus,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[list[UserContentList], int]:
        count_result = await db.execute(
            select(func.count(UserContentList.id)).where(
                UserContentList.user_id == user_id,
                UserContentList.status == status
            )
        )
        total = count_result.scalar() or 0

        result = await db.execute(
            select(UserContentList)
            .where(
                UserContentList.user_id == user_id,
                UserContentList.status == status
            )
            .order_by(desc(UserContentList.id))
            .offset(skip)
            .limit(limit)
        )
        entries = result.scalars().all()
        return list(entries), total

    @staticmethod
    async def get_user_lists_grouped(
        db: AsyncSession,
        user_id: UUID
    ) -> dict[str, list[UserContentList]]:
        result = await db.execute(
            select(UserContentList)
            .where(UserContentList.user_id == user_id)
            .order_by(desc(UserContentList.id))
        )
        entries = result.scalars().all()

        grouped = {
            'completed': [],
            'planned': [],
            'dropped': []
        }

        for entry in entries:
            grouped[entry.status.value].append(entry)

        return grouped

    @staticmethod
    async def get_user_stats(
        db: AsyncSession,
        user_id: UUID
    ) -> dict:
        result = await db.execute(
            select(
                UserContentList.status,
                func.count(UserContentList.id).label('count')
            )
            .where(UserContentList.user_id == user_id)
            .group_by(UserContentList.status)
        )
        
        stats = result.fetchall()
        
        counts = {
            'completed_count': 0,
            'planned_count': 0,
            'dropped_count': 0
        }

        for status, count in stats:
            if status == WatchStatus.COMPLETED:
                counts['completed_count'] = count
            elif status == WatchStatus.PLANNED:
                counts['planned_count'] = count
            elif status == WatchStatus.DROPPED:
                counts['dropped_count'] = count

        return counts