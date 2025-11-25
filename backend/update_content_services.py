#!/usr/bin/env python3
"""Script to update all content services with filtering capabilities"""

SERVICES_TO_UPDATE = [
    {
        'name': 'Film',
        'file': 'src/app/content/services/film_service.py',
        'filter_params': 'FilmFilterParams',
        'additional_filters': """
        if filters.director is not None:
            additional_filters['director'] = filters.director

        if filters.min_duration is not None or filters.max_duration is not None:
            additional_filters['duration_minutes'] = {}
            if filters.min_duration is not None:
                additional_filters['duration_minutes']['min'] = filters.min_duration
            if filters.max_duration is not None:
                additional_filters['duration_minutes']['max'] = filters.max_duration
""",
    },
    {
        'name': 'Series',
        'file': 'src/app/content/services/series_service.py',
        'filter_params': 'SeriesFilterParams',
        'additional_filters': """
        if filters.is_ongoing is not None:
            additional_filters['is_ongoing'] = filters.is_ongoing

        if filters.season is not None:
            additional_filters['season'] = filters.season

        if filters.min_episodes is not None or filters.max_episodes is not None:
            additional_filters['total_episodes'] = {}
            if filters.min_episodes is not None:
                additional_filters['total_episodes']['min'] = filters.min_episodes
            if filters.max_episodes is not None:
                additional_filters['total_episodes']['max'] = filters.max_episodes
""",
    },
    {
        'name': 'Anime',
        'file': 'src/app/content/services/anime_service.py',
        'filter_params': 'AnimeFilterParams',
        'additional_filters': """
        if filters.is_ongoing is not None:
            additional_filters['is_ongoing'] = filters.is_ongoing

        if filters.studio is not None:
            additional_filters['studio'] = filters.studio

        if filters.min_episodes is not None or filters.max_episodes is not None:
            additional_filters['total_episodes'] = {}
            if filters.min_episodes is not None:
                additional_filters['total_episodes']['min'] = filters.min_episodes
            if filters.max_episodes is not None:
                additional_filters['total_episodes']['max'] = filters.max_episodes
""",
    },
    {
        'name': 'Podcast',
        'file': 'src/app/content/services/podcast_service.py',
        'filter_params': 'PodcastFilterParams',
        'additional_filters': """
        if filters.is_ongoing is not None:
            additional_filters['is_ongoing'] = filters.is_ongoing

        if filters.host is not None:
            additional_filters['host'] = filters.host

        if filters.min_episodes is not None or filters.max_episodes is not None:
            additional_filters['total_episodes'] = {}
            if filters.min_episodes is not None:
                additional_filters['total_episodes']['min'] = filters.min_episodes
            if filters.max_episodes is not None:
                additional_filters['total_episodes']['max'] = filters.max_episodes
""",
    },
    {
        'name': 'Course',
        'file': 'src/app/content/services/course_service.py',
        'filter_params': 'CourseFilterParams',
        'additional_filters': """
        if filters.difficulty_level is not None:
            additional_filters['difficulty_level'] = filters.difficulty_level

        if filters.instructor is not None:
            additional_filters['instructor'] = filters.instructor

        if filters.min_lessons is not None or filters.max_lessons is not None:
            additional_filters['total_lessons'] = {}
            if filters.min_lessons is not None:
                additional_filters['total_lessons']['min'] = filters.min_lessons
            if filters.max_lessons is not None:
                additional_filters['total_lessons']['max'] = filters.max_lessons

        if filters.min_duration_hours is not None or filters.max_duration_hours is not None:
            additional_filters['total_duration_hours'] = {}
            if filters.min_duration_hours is not None:
                additional_filters['total_duration_hours']['min'] = filters.min_duration_hours
            if filters.max_duration_hours is not None:
                additional_filters['total_duration_hours']['max'] = filters.max_duration_hours
""",
    },
    {
        'name': 'Article',
        'file': 'src/app/content/services/article_service.py',
        'filter_params': 'ArticleFilterParams',
        'additional_filters': """
        if filters.is_published is not None:
            additional_filters['is_published'] = filters.is_published

        if filters.min_word_count is not None or filters.max_word_count is not None:
            additional_filters['word_count'] = {}
            if filters.min_word_count is not None:
                additional_filters['word_count']['min'] = filters.min_word_count
            if filters.max_word_count is not None:
                additional_filters['word_count']['max'] = filters.max_word_count

        if filters.min_reading_time is not None or filters.max_reading_time is not None:
            additional_filters['reading_time_minutes'] = {}
            if filters.min_reading_time is not None:
                additional_filters['reading_time_minutes']['min'] = filters.min_reading_time
            if filters.max_reading_time is not None:
                additional_filters['reading_time_minutes']['max'] = filters.max_reading_time
""",
    },
    {
        'name': 'Game',
        'file': 'src/app/content/services/game_service.py',
        'filter_params': 'GameFilterParams',
        'additional_filters': """
        if filters.developer is not None:
            additional_filters['developer'] = filters.developer

        if filters.publisher is not None:
            additional_filters['publisher'] = filters.publisher

        if filters.genre is not None:
            additional_filters['genre'] = filters.genre

        if filters.is_multiplayer is not None:
            additional_filters['is_multiplayer'] = filters.is_multiplayer
""",
    },
    {
        'name': 'Video',
        'file': 'src/app/content/services/video_service.py',
        'filter_params': 'VideoFilterParams',
        'additional_filters': """
        if filters.creator is not None:
            additional_filters['creator'] = filters.creator

        if filters.min_duration is not None or filters.max_duration is not None:
            additional_filters['duration_minutes'] = {}
            if filters.min_duration is not None:
                additional_filters['duration_minutes']['min'] = filters.min_duration
            if filters.max_duration is not None:
                additional_filters['duration_minutes']['max'] = filters.max_duration
""",
    },
]


def generate_service_method(name: str, filter_params: str, additional_filters: str) -> str:
    """Generate the get_filtered method for a service"""
    name_lower = name.lower()
    name_plural = name.lower() + 's' if not name.lower().endswith('s') else name.lower() + 'es'

    return f'''    @staticmethod
    async def get_filtered(
        db: AsyncSession, filters: {filter_params}, skip: int = 0, limit: int = 100
    ) -> tuple[list[{name}Read], int]:
        """Get filtered {name_plural} with pagination"""
        # Build additional {name_lower}-specific filters
        additional_filters = {{}}{additional_filters}
        # Get filtered {name_plural}
        {name_plural}, total = await ContentRepository.get_filtered(
            db, {name}, filters, skip=skip, limit=limit, additional_filters=additional_filters
        )

        return [{name}Read.model_validate({name_lower}) for {name_lower} in {name_plural}], total
'''


if __name__ == '__main__':
    print('Service update configuration:')
    for service in SERVICES_TO_UPDATE:
        print(f'  - {service["name"]} ({service["filter_params"]})')

    print('\nGenerated methods can be added to respective service files.')
    print('\nFor each service, add the import:')
    print('from app.content.schemas.filters import <FilterParams>')
    print('\nAnd add this method after get_all():')
    for service in SERVICES_TO_UPDATE:
        print(f'\n# {service["name"]}Service:')
        print(generate_service_method(service['name'], service['filter_params'], service['additional_filters']))
