from .age_ratings_router import router as age_ratings_router
from .authors_router import router as authors_router
from .content_categories_router import router as content_categories_router
from .content_statuses_router import router as content_statuses_router
from .content_types_router import router as content_types_router
from .countries_router import router as countries_router
from .difficulty_levels_router import router as difficulty_levels_router
from .genres_router import router as genres_router
from .languages_router import router as languages_router
from .platforms_router import router as platforms_router
from .tags_router import router as tags_router

__all__ = [
    'tags_router',
    'content_types_router',
    'genres_router',
    'countries_router',
    'languages_router',
    'authors_router',
    'platforms_router',
    'age_ratings_router',
    'difficulty_levels_router',
    'content_statuses_router',
    'content_categories_router',
]

