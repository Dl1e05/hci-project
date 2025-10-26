from sqlalchemy import Integer, String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.content.models.base import BaseContent


class Series(BaseContent):
    __tablename__ = "series"

    total_episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    current_episode: Mapped[int] = mapped_column(Integer, nullable=True, default=1)
    season: Mapped[int] = mapped_column(Integer, nullable=True, default=1)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Book(BaseContent):
    __tablename__ = "books"
    
    # Book-specific fields
    pages: Mapped[int] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str] = mapped_column(String(20), nullable=True, unique=True, index=True)
    edition: Mapped[str] = mapped_column(String(50), nullable=True)
    publisher: Mapped[str] = mapped_column(String(100), nullable=True)


class Film(BaseContent):
    __tablename__ = "films"

    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    director: Mapped[str] = mapped_column(String(100), nullable=True)


class Anime(BaseContent):
    __tablename__ = "animes"

    total_episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    seasons: Mapped[int] = mapped_column(Integer, nullable=True, default=1)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    studio: Mapped[str] = mapped_column(String(100), nullable=True)


class Podcast(BaseContent):
    __tablename__ = "podcasts"

    total_episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    average_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    host: Mapped[str] = mapped_column(String(100), nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Course(BaseContent):
    __tablename__ = "courses"

    total_lessons: Mapped[int] = mapped_column(Integer, nullable=True)
    total_duration_hours: Mapped[float] = mapped_column(Float, nullable=True)
    difficulty_level: Mapped[str] = mapped_column(String(20), nullable=True)
    instructor: Mapped[str] = mapped_column(String(100), nullable=True)


class Article(BaseContent):
    __tablename__ = "articles"

    word_count: Mapped[int] = mapped_column(Integer, nullable=True)
    reading_time_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class Game(BaseContent):
    __tablename__ = "games"

    developer: Mapped[str] = mapped_column(String(100), nullable=True)
    publisher: Mapped[str] = mapped_column(String(100), nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=True)
    is_multiplayer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)



class Video(BaseContent):
    __tablename__ = "videos"

    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    creator: Mapped[str] = mapped_column(String(100), nullable=True)



