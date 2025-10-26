import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, Table, Float, ForeignKey, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.references.models import Language, Genres, Country, AgeRating, Author, Tags

from app.base import Base

if TYPE_CHECKING:
    from app.references.models import Language, Genres, Country, AgeRating, Author, Tags


content_genres = Table(
    'content_genres',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', PG_UUID(as_uuid=True), ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
)

content_audio_languages = Table(
    'content_audio_languages',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id', ondelete='CASCADE'), primary_key=True),
)

content_subtitle_languages = Table(
    'content_subtitle_languages',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('language_id', Integer, ForeignKey('languages.id', ondelete='CASCADE'), primary_key=True),
)

content_tags = Table(
    'content_tags',
    Base.metadata,
    Column('content_id', PG_UUID(as_uuid=True), ForeignKey('contents.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', PG_UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
)


class BaseContent(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    release_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    rating: Mapped[float]   = mapped_column(Float, nullable=False, index=True)

    view_count: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    short_description: Mapped[str] = mapped_column(String(500), nullable=True)
    long_description: Mapped[str] = mapped_column(Text, nullable=True)
    
    tags: Mapped[str] = mapped_column(String(500), nullable=True)
    keywords: Mapped[str] = mapped_column(String(500), nullable=True)
    
    original_language_id: Mapped[int] = mapped_column(Integer, ForeignKey('languages.id'), nullable=False, index=True)
    age_rating_id: Mapped[int] = mapped_column(Integer, ForeignKey('age_ratings.id'), nullable=False, index=True)
    original_author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'), nullable=False, index=True)
    country_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey('countries.id'), nullable=False, index=True)

    banner: Mapped[str] = mapped_column(URLType(length=2048), nullable=False)
    trailer: Mapped[str] = mapped_column(URLType(length=2048), nullable=True)
    link: Mapped[str] = mapped_column(URLType(length=2048), nullable=True)
    poster: Mapped[str] = mapped_column(URLType(length=2048), nullable=True)


    original_language: Mapped["Language"] = relationship("Language", foreign_keys=[original_language_id], back_populates="contents")
    age_rating: Mapped["AgeRating"] = relationship("AgeRating", back_populates="contents")
    original_author: Mapped['Author'] = relationship("Author", back_populates="contents")
    country: Mapped["Country"] = relationship("Country", back_populates="contents")

    genres: Mapped[list["Genres"]] = relationship("Genres", secondary=content_genres, back_populates="contents")
    audio_languages: Mapped[list["Language"]] = relationship("Language", secondary=content_audio_languages, back_populates="audio_contents")
    subtitle_languages: Mapped[list["Language"]] = relationship("Language", secondary=content_subtitle_languages, back_populates="subtitle_contents")
    content_tags: Mapped[list["Tags"]] = relationship("Tags", secondary=content_tags, back_populates="contents")


