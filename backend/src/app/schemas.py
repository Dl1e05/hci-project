"""
Comprehensive Pydantic schemas for the HCI project.

This module provides all Pydantic schemas based on the SQLAlchemy models.
All schemas inherit from ORMModel which provides proper configuration for
SQLAlchemy integration with Pydantic.
"""

# Content schemas
from app.content.schemas import (
    BaseContentBase, BaseContentCreate, BaseContentUpdate, BaseContentRead,
    SeriesBase, SeriesCreate, SeriesUpdate, SeriesRead,
    BookBase, BookCreate, BookUpdate, BookRead,
    FilmBase, FilmCreate, FilmUpdate, FilmRead,
    AnimeBase, AnimeCreate, AnimeUpdate, AnimeRead,
    PodcastBase, PodcastCreate, PodcastUpdate, PodcastRead,
    CourseBase, CourseCreate, CourseUpdate, CourseRead,
    ArticleBase, ArticleCreate, ArticleUpdate, ArticleRead,
    GameBase, GameCreate, GameUpdate, GameRead,
    VideoBase, VideoCreate, VideoUpdate, VideoRead,
)

# Reference schemas
from app.references.schemas import (
    TagsBase, TagsCreate, TagsUpdate, TagsRead,
    ContentTypeBase, ContentTypeCreate, ContentTypeUpdate, ContentTypeRead,
    GenresBase, GenresCreate, GenresUpdate, GenresRead,
    CountryBase, CountryCreate, CountryUpdate, CountryRead,
    LanguageBase, LanguageCreate, LanguageUpdate, LanguageRead,
    AuthorBase, AuthorCreate, AuthorUpdate, AuthorRead,
    PlatformBase, PlatformCreate, PlatformUpdate, PlatformRead,
    AgeRatingBase, AgeRatingCreate, AgeRatingUpdate, AgeRatingRead,
    DifficultyLevelBase, DifficultyLevelCreate, DifficultyLevelUpdate, DifficultyLevelRead,
    ContentStatusBase, ContentStatusCreate, ContentStatusUpdate, ContentStatusRead,
    ContentCategoryBase, ContentCategoryCreate, ContentCategoryUpdate, ContentCategoryRead,
)

# User schemas
from app.users.schemas import (
    UserBase, UserCreate, UserUpdate, UserRead,
)

# User interaction schemas
from app.users.schemas.user_interactions import (
    UserRatingBase, UserRatingCreate, UserRatingUpdate, UserRatingRead,
    UserProgressBase, UserProgressCreate, UserProgressUpdate, UserProgressRead,
)

__all__ = [
    # Content schemas
    "BaseContentBase", "BaseContentCreate", "BaseContentUpdate", "BaseContentRead",
    "SeriesBase", "SeriesCreate", "SeriesUpdate", "SeriesRead",
    "BookBase", "BookCreate", "BookUpdate", "BookRead",
    "FilmBase", "FilmCreate", "FilmUpdate", "FilmRead",
    "AnimeBase", "AnimeCreate", "AnimeUpdate", "AnimeRead",
    "PodcastBase", "PodcastCreate", "PodcastUpdate", "PodcastRead",
    "CourseBase", "CourseCreate", "CourseUpdate", "CourseRead",
    "ArticleBase", "ArticleCreate", "ArticleUpdate", "ArticleRead",
    "GameBase", "GameCreate", "GameUpdate", "GameRead",
    "VideoBase", "VideoCreate", "VideoUpdate", "VideoRead",
    
    # Reference schemas
    "TagsBase", "TagsCreate", "TagsUpdate", "TagsRead",
    "ContentTypeBase", "ContentTypeCreate", "ContentTypeUpdate", "ContentTypeRead",
    "GenresBase", "GenresCreate", "GenresUpdate", "GenresRead",
    "CountryBase", "CountryCreate", "CountryUpdate", "CountryRead",
    "LanguageBase", "LanguageCreate", "LanguageUpdate", "LanguageRead",
    "AuthorBase", "AuthorCreate", "AuthorUpdate", "AuthorRead",
    "PlatformBase", "PlatformCreate", "PlatformUpdate", "PlatformRead",
    "AgeRatingBase", "AgeRatingCreate", "AgeRatingUpdate", "AgeRatingRead",
    "DifficultyLevelBase", "DifficultyLevelCreate", "DifficultyLevelUpdate", "DifficultyLevelRead",
    "ContentStatusBase", "ContentStatusCreate", "ContentStatusUpdate", "ContentStatusRead",
    "ContentCategoryBase", "ContentCategoryCreate", "ContentCategoryUpdate", "ContentCategoryRead",
    
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "UserRead",
    
    # User interaction schemas
    "UserRatingBase", "UserRatingCreate", "UserRatingUpdate", "UserRatingRead",
    "UserProgressBase", "UserProgressCreate", "UserProgressUpdate", "UserProgressRead",
]

