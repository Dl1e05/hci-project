from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination query parameters"""

    skip: int = Field(default=0, ge=0, description='Number of records to skip')
    limit: int = Field(default=100, ge=1, le=1000, description='Maximum number of records to return')


class PaginatedResponse[T](BaseModel):
    """Generic paginated response"""

    items: list[T] = Field(description='List of items')
    total: int = Field(description='Total number of items matching the filters')
    skip: int = Field(description='Number of records skipped')
    limit: int = Field(description='Maximum number of records returned')
    has_more: bool = Field(description='Whether there are more items available')

    @classmethod
    def create(cls, items: list[T], total: int, skip: int, limit: int) -> 'PaginatedResponse[T]':
        """Create a paginated response"""
        return cls(items=items, total=total, skip=skip, limit=limit, has_more=skip + len(items) < total)
