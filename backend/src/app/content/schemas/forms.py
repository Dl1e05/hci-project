from datetime import datetime
from uuid import UUID

from fastapi import Form

from .content import (
    AnimeCreate,
    ArticleCreate,
    BookCreate,
    CourseCreate,
    FilmCreate,
    GameCreate,
    PodcastCreate,
    SeriesCreate,
    VideoCreate,
)


def parse_list_field(value: list[str] | str | None, field_name: str = 'field') -> list[str]:  # noqa: ARG001
    if not value:
        return []

    if isinstance(value, str):
        # Handle comma-separated string
        return [item.strip() for item in value.split(',') if item.strip()]

    # Handle list
    result = []
    for item in value:
        if not item:
            continue
        # Check if the item itself is a comma-separated string
        if isinstance(item, str) and ',' in item:
            # Split it further
            result.extend([sub_item.strip() for sub_item in item.split(',') if sub_item.strip()])
        else:
            item_str = item.strip() if isinstance(item, str) else str(item)
            if item_str:
                result.append(item_str)
    return result


class BookFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        pages: int | None = Form(None),
        isbn: str | None = Form(None),
        edition: str | None = Form(None),
        publisher: str | None = Form(None),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.difficulty_level_id = difficulty_level_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.pages = pages
        self.isbn = isbn
        self.edition = edition
        self.publisher = publisher

    def to_schema(self, banner_url: str) -> BookCreate:
        return BookCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            pages=self.pages,
            isbn=self.isbn,
            edition=self.edition,
            publisher=self.publisher,
        )


class FilmFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        duration_minutes: int | None = Form(None),
        director: str | None = Form(None),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.duration_minutes = duration_minutes
        self.director = director

    def to_schema(self, banner_url: str) -> FilmCreate:
        return FilmCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            duration_minutes=self.duration_minutes,
            director=self.director,
        )


class SeriesFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        total_episodes: int | None = Form(None),
        current_episode: int | None = Form(None),
        season: int | None = Form(None),
        is_ongoing: bool = Form(True),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.total_episodes = total_episodes
        self.current_episode = current_episode
        self.season = season
        self.is_ongoing = is_ongoing

    def to_schema(self, banner_url: str) -> SeriesCreate:
        return SeriesCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            total_episodes=self.total_episodes,
            current_episode=self.current_episode,
            season=self.season,
            is_ongoing=self.is_ongoing,
        )


class AnimeFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        total_episodes: int | None = Form(None),
        seasons: int | None = Form(None),
        is_ongoing: bool = Form(True),
        studio: str | None = Form(None),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.total_episodes = total_episodes
        self.seasons = seasons
        self.is_ongoing = is_ongoing
        self.studio = studio

    def to_schema(self, banner_url: str) -> AnimeCreate:
        return AnimeCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            total_episodes=self.total_episodes,
            seasons=self.seasons,
            is_ongoing=self.is_ongoing,
            studio=self.studio,
        )


class PodcastFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        total_episodes: int | None = Form(None),
        average_duration_minutes: int | None = Form(None),
        host: str | None = Form(None),
        is_ongoing: bool = Form(True),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.total_episodes = total_episodes
        self.average_duration_minutes = average_duration_minutes
        self.host = host
        self.is_ongoing = is_ongoing

    def to_schema(self, banner_url: str) -> PodcastCreate:
        return PodcastCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            total_episodes=self.total_episodes,
            average_duration_minutes=self.average_duration_minutes,
            host=self.host,
            is_ongoing=self.is_ongoing,
        )


class CourseFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        total_lessons: int | None = Form(None),
        total_duration_hours: float | None = Form(None),
        course_difficulty: str | None = Form(None),
        instructor: str | None = Form(None),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.total_lessons = total_lessons
        self.total_duration_hours = total_duration_hours
        self.course_difficulty = course_difficulty
        self.instructor = instructor

    def to_schema(self, banner_url: str) -> CourseCreate:
        return CourseCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            total_lessons=self.total_lessons,
            total_duration_hours=self.total_duration_hours,
            course_difficulty=self.course_difficulty,
            instructor=self.instructor,
        )


class ArticleFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        word_count: int | None = Form(None),
        reading_time_minutes: int | None = Form(None),
        is_published: bool = Form(True),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.word_count = word_count
        self.reading_time_minutes = reading_time_minutes
        self.is_published = is_published

    def to_schema(self, banner_url: str) -> ArticleCreate:
        return ArticleCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            word_count=self.word_count,
            reading_time_minutes=self.reading_time_minutes,
            is_published=self.is_published,
        )


class GameFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        developer: str | None = Form(None),
        publisher: str | None = Form(None),
        genre: str | None = Form(None),
        is_multiplayer: bool = Form(False),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.developer = developer
        self.publisher = publisher
        self.genre = genre
        self.is_multiplayer = is_multiplayer

    def to_schema(self, banner_url: str) -> GameCreate:
        return GameCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            developer=self.developer,
            publisher=self.publisher,
            genre=self.genre,
            is_multiplayer=self.is_multiplayer,
        )


class VideoFormData:
    def __init__(
        self,
        title: str = Form(...),
        release_date: datetime = Form(...),
        original_language_id: int = Form(...),
        difficulty_level_id: int = Form(...),
        age_rating_id: int = Form(...),
        original_author_id: int = Form(...),
        country_id: UUID = Form(...),
        is_active: bool = Form(True),
        short_description: str | None = Form(None),
        long_description: str | None = Form(None),
        keywords: str | None = Form(None),
        trailer: str | None = Form(None),
        link: str | None = Form(None),
        genre_ids: str | list[str] = Form(default=''),
        audio_language_ids: str | list[str] = Form(default=''),
        subtitle_language_ids: str | list[str] = Form(default=''),
        tag_ids: str | list[str] = Form(default=''),
        duration_minutes: int | None = Form(None),
        creator: str | None = Form(None),
    ):
        parsed_genre_ids = parse_list_field(genre_ids, 'genre_ids')
        parsed_audio_ids = parse_list_field(audio_language_ids, 'audio_language_ids')
        parsed_subtitle_ids = parse_list_field(subtitle_language_ids, 'subtitle_language_ids')
        parsed_tag_ids = parse_list_field(tag_ids, 'tag_ids')

        try:
            self.genre_ids = [UUID(id) for id in parsed_genre_ids] if parsed_genre_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in genre_ids: {parsed_genre_ids}. Error: {e}') from e

        try:
            self.audio_language_ids = [int(id) for id in parsed_audio_ids] if parsed_audio_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in audio_language_ids: {parsed_audio_ids}. Error: {e}') from e

        try:
            self.subtitle_language_ids = [int(id) for id in parsed_subtitle_ids] if parsed_subtitle_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid integer in subtitle_language_ids: {parsed_subtitle_ids}. Error: {e}') from e

        try:
            self.tag_ids = [UUID(id) for id in parsed_tag_ids] if parsed_tag_ids else []
        except ValueError as e:
            raise ValueError(f'Invalid UUID in tag_ids: {parsed_tag_ids}. Error: {e}') from e

        self.title = title
        self.release_date = release_date
        self.original_language_id = original_language_id
        self.difficulty_level_id = difficulty_level_id
        self.age_rating_id = age_rating_id
        self.original_author_id = original_author_id
        self.country_id = country_id
        self.is_active = is_active
        self.short_description = short_description
        self.long_description = long_description
        self.keywords = keywords
        self.trailer = trailer
        self.link = link
        self.duration_minutes = duration_minutes
        self.creator = creator

    def to_schema(self, banner_url: str) -> VideoCreate:
        return VideoCreate(
            title=self.title,
            release_date=self.release_date,
            is_active=self.is_active,
            short_description=self.short_description,
            long_description=self.long_description,
            keywords=self.keywords,
            banner=banner_url,
            trailer=self.trailer,
            link=self.link,
            original_language_id=self.original_language_id,
            difficulty_level_id=self.difficulty_level_id,
            age_rating_id=self.age_rating_id,
            original_author_id=self.original_author_id,
            country_id=self.country_id,
            genre_ids=self.genre_ids,
            audio_language_ids=self.audio_language_ids,
            subtitle_language_ids=self.subtitle_language_ids,
            tag_ids=self.tag_ids,
            duration_minutes=self.duration_minutes,
            creator=self.creator,
        )
