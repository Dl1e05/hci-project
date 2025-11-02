from .base import (
    BaseContentBase,
    BaseContentCreate,
    BaseContentRead,
    BaseContentUpdate,
)
from .content import (
    # Anime schemas
    AnimeCreate,
    AnimeRead,
    AnimeUpdate,
    # Article schemas
    ArticleCreate,
    ArticleRead,
    ArticleUpdate,
    # Book schemas
    BookCreate,
    BookRead,
    BookUpdate,
    # Course schemas
    CourseCreate,
    CourseRead,
    CourseUpdate,
    # Film schemas
    FilmCreate,
    FilmRead,
    FilmUpdate,
    # Game schemas
    GameCreate,
    GameRead,
    GameUpdate,
    # Podcast schemas
    PodcastCreate,
    PodcastRead,
    PodcastUpdate,
    # Series schemas
    SeriesCreate,
    SeriesRead,
    SeriesUpdate,
    # Video schemas
    VideoCreate,
    VideoRead,
    VideoUpdate,
)

__all__ = [
    # Base content schemas
    'BaseContentBase',
    'BaseContentCreate',
    'BaseContentUpdate',
    'BaseContentRead',
    # Series schemas
    'SeriesCreate',
    'SeriesUpdate',
    'SeriesRead',
    # Book schemas
    'BookCreate',
    'BookUpdate',
    'BookRead',
    # Film schemas
    'FilmCreate',
    'FilmUpdate',
    'FilmRead',
    # Anime schemas
    'AnimeCreate',
    'AnimeUpdate',
    'AnimeRead',
    # Podcast schemas
    'PodcastCreate',
    'PodcastUpdate',
    'PodcastRead',
    # Course schemas
    'CourseCreate',
    'CourseUpdate',
    'CourseRead',
    # Article schemas
    'ArticleCreate',
    'ArticleUpdate',
    'ArticleRead',
    # Game schemas
    'GameCreate',
    'GameUpdate',
    'GameRead',
    # Video schemas
    'VideoCreate',
    'VideoUpdate',
    'VideoRead',
]
