import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.content.models.content import Anime, Article, Book, Course, Film, Game, Podcast, Series, Video
from app.core.db import AsyncSessionLocal
from app.references.models import AgeRating, Author, Country, DifficultyLevel, Genres, Language, Tags


async def get_or_create_references(db: AsyncSession):
    result = await db.execute(select(Language))
    languages = list(result.scalars().all())
    if not languages:
        print('No languages found. Please seed reference data first.')
        return None

    result = await db.execute(select(AgeRating))
    age_ratings = list(result.scalars().all())
    if not age_ratings:
        print('No age ratings found. Please seed reference data first.')
        return None

    result = await db.execute(select(Author))
    authors = list(result.scalars().all())
    if not authors:
        print('No authors found. Please seed reference data first.')
        return None

    result = await db.execute(select(Country))
    countries = list(result.scalars().all())
    if not countries:
        print('No countries found. Please seed reference data first.')
        return None

    result = await db.execute(select(DifficultyLevel))
    difficulty_levels = list(result.scalars().all())
    if not difficulty_levels:
        print('No difficulty levels found. Please seed reference data first.')
        return None

    result = await db.execute(select(Genres))
    genres = list(result.scalars().all())

    result = await db.execute(select(Tags))
    tags = list(result.scalars().all())

    return {
        'languages': languages,
        'age_ratings': age_ratings,
        'authors': authors,
        'countries': countries,
        'difficulty_levels': difficulty_levels,
        'genres': genres,
        'tags': tags,
    }


async def seed_content():
    async with AsyncSessionLocal() as db:
        refs = await get_or_create_references(db)
        if not refs:
            return

        lang_en = next((lang for lang in refs['languages'] if lang.code == 'en'), refs['languages'][0])
        lang_ja = next((lang for lang in refs['languages'] if lang.code == 'ja'), refs['languages'][0])

        series_list = [
            Series(
                title='Breaking Bad',
                release_date=datetime(2008, 1, 20),
                _rating=9.5,
                view_count=15000,
                is_active=True,
                short_description='A chemistry teacher turns to cooking meth after a cancer diagnosis',
                long_description=(
                    'Walter White, a high school chemistry teacher, is diagnosed with terminal lung cancer. '
                    "To secure his family's financial future, he teams up with former student Jesse Pinkman "
                    'to produce and sell methamphetamine.'
                ),
                keywords='crime, drama, drugs, chemistry, family',
                banner='https://example.com/breaking-bad-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_episodes=62,
                current_episode=1,
                season=5,
                is_ongoing=False,
            ),
            Series(
                title='Stranger Things',
                release_date=datetime(2016, 7, 15),
                _rating=8.7,
                view_count=12000,
                is_active=True,
                short_description='Kids in a small town uncover supernatural mysteries and secret experiments',
                long_description=(
                    'When a young boy disappears, his mother, friends, and the local police chief uncover '
                    'a mystery involving secret experiments, terrifying supernatural forces, and a strange little girl.'
                ),
                keywords='supernatural, sci-fi, horror, friendship, 80s',
                banner='https://example.com/stranger-things-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_episodes=42,
                current_episode=1,
                season=4,
                is_ongoing=True,
            ),
        ]

        book_list = [
            Book(
                title='The Great Gatsby',
                release_date=datetime(1925, 4, 10),
                _rating=8.2,
                view_count=8000,
                is_active=True,
                short_description='A mysterious millionaire and his obsession with a former lover',
                long_description=(
                    'Set in the Jazz Age, this novel tells the story of Jay Gatsby and his unrequited love for '
                    'Daisy Buchanan, exploring themes of decadence, idealism, and excess.'
                ),
                keywords='classic, romance, american dream, jazz age',
                banner='https://example.com/great-gatsby-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                pages=180,
                isbn='978-0743273565',
                edition='Scribner',
                publisher='Scribner',
            ),
            Book(
                title='1984',
                release_date=datetime(1949, 6, 8),
                _rating=8.9,
                view_count=10000,
                is_active=True,
                short_description='Dystopian novel about totalitarianism and surveillance',
                long_description=(
                    'Winston Smith works for the Ministry of Truth in Oceania, rewriting history. '
                    'He begins a forbidden love affair and joins a resistance movement against the oppressive Party led by Big Brother.'
                ),
                keywords='dystopia, totalitarianism, surveillance, freedom, politics',
                banner='https://example.com/1984-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                pages=328,
                isbn='978-0451524935',
                edition='Signet Classic',
                publisher='Signet Classic',
            ),
        ]

        film_list = [
            Film(
                title='The Shawshank Redemption',
                release_date=datetime(1994, 9, 23),
                _rating=9.3,
                view_count=20000,
                is_active=True,
                short_description='Two imprisoned men bond over years, finding redemption',
                long_description=(
                    'Andy Dufresne is sentenced to life in Shawshank State Penitentiary for murders he did not commit. '
                    'Over the years, he forms a friendship with Red and finds ways to survive and ultimately transcend his situation.'
                ),
                keywords='prison, friendship, hope, redemption, drama',
                banner='https://example.com/shawshank-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                duration_minutes=142,
                director='Frank Darabont',
            ),
            Film(
                title='Inception',
                release_date=datetime(2010, 7, 16),
                _rating=8.8,
                view_count=18000,
                is_active=True,
                short_description='A thief who steals secrets through dreams gets a chance at redemption',
                long_description=(
                    "Dom Cobb is a skilled thief who extracts secrets from people's subconscious during the dream state. "
                    'He is offered a chance to have his criminal history erased as payment for implanting an idea into '
                    "a target's subconscious."
                ),
                keywords='sci-fi, dreams, heist, action, mind-bending',
                banner='https://example.com/inception-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                duration_minutes=148,
                director='Christopher Nolan',
            ),
        ]

        anime_list = [
            Anime(
                title='Attack on Titan',
                release_date=datetime(2013, 4, 7),
                _rating=9.0,
                view_count=25000,
                is_active=True,
                short_description='Humanity fights for survival against giant humanoid Titans',
                long_description=(
                    'In a world where humanity lives inside cities surrounded by enormous walls due to the Titans, '
                    'gigantic humanoid creatures who devour humans seemingly without reason, Eren Yeager vows to '
                    'exterminate them after they destroy his hometown.'
                ),
                keywords='action, dark fantasy, post-apocalyptic, shounen, war',
                banner='https://example.com/aot-banner.jpg',
                original_language_id=lang_ja.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_episodes=87,
                seasons=4,
                is_ongoing=False,
                studio='MAPPA',
            ),
            Anime(
                title='Death Note',
                release_date=datetime(2006, 10, 4),
                _rating=9.0,
                view_count=22000,
                is_active=True,
                short_description='High school student finds a supernatural notebook',
                long_description=(
                    'Light Yagami discovers a mysterious notebook that allows him to kill anyone by writing their name in it. '
                    'He decides to create a utopia by eliminating criminals, but a detective known as L begins to track him down.'
                ),
                keywords='psychological, thriller, supernatural, cat and mouse, morality',
                banner='https://example.com/death-note-banner.jpg',
                original_language_id=lang_ja.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_episodes=37,
                seasons=1,
                is_ongoing=False,
                studio='Madhouse',
            ),
        ]

        podcast_list = [
            Podcast(
                title='The Joe Rogan Experience',
                release_date=datetime(2009, 12, 24),
                _rating=8.5,
                view_count=30000,
                is_active=True,
                short_description='Long-form conversations with diverse guests',
                long_description=(
                    'Joe Rogan hosts long-form conversations with guests from various backgrounds including '
                    'comedians, actors, musicians, MMA fighters, authors, and scientists discussing a wide range of topics.'
                ),
                keywords='comedy, interview, culture, science, philosophy',
                banner='https://example.com/jre-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_episodes=2000,
                average_duration_minutes=180,
                host='Joe Rogan',
                is_ongoing=True,
            ),
        ]

        course_list = [
            Course(
                title='Python for Data Science',
                release_date=datetime(2020, 1, 15),
                _rating=8.8,
                view_count=5000,
                is_active=True,
                short_description='Learn Python programming for data analysis and machine learning',
                long_description=(
                    'Comprehensive course covering Python fundamentals, data manipulation with Pandas, '
                    'data visualization, statistical analysis, and introduction to machine learning with scikit-learn.'
                ),
                keywords='python, data science, machine learning, programming, analytics',
                banner='https://example.com/python-ds-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][1].id
                if len(refs['difficulty_levels']) > 1
                else refs['difficulty_levels'][0].id,
                total_lessons=120,
                total_duration_hours=40.5,
                instructor='Dr. Sarah Johnson',
            ),
            Course(
                title='Web Development Bootcamp',
                release_date=datetime(2021, 3, 10),
                _rating=9.2,
                view_count=7000,
                is_active=True,
                short_description='Complete web development from frontend to backend',
                long_description=(
                    'Master HTML, CSS, JavaScript, React, Node.js, Express, MongoDB, and deployment. '
                    'Build real-world projects and portfolio-ready applications.'
                ),
                keywords='web development, javascript, react, node, fullstack',
                banner='https://example.com/webdev-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                total_lessons=200,
                total_duration_hours=65.0,
                instructor='Colt Steele',
            ),
        ]

        article_list = [
            Article(
                title='The Future of Artificial Intelligence',
                release_date=datetime(2024, 1, 15),
                _rating=8.3,
                view_count=4000,
                is_active=True,
                short_description='Exploring the developments and implications of AI technology',
                long_description=(
                    'An in-depth analysis of recent breakthroughs in artificial intelligence, '
                    'including large language models, computer vision, and their potential impact on society, economy, and daily life.'
                ),
                keywords='AI, technology, future, machine learning, innovation',
                banner='https://example.com/ai-future-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                word_count=3500,
                reading_time_minutes=15,
                is_published=True,
            ),
        ]

        game_list = [
            Game(
                title='The Witcher 3: Wild Hunt',
                release_date=datetime(2015, 5, 19),
                _rating=9.4,
                view_count=28000,
                is_active=True,
                short_description='Epic fantasy RPG following monster hunter Geralt of Rivia',
                long_description=(
                    'Play as Geralt of Rivia, a professional monster hunter searching for his adopted daughter in a vast open world '
                    'filled with merchant cities, dangerous mountain passes, and forgotten caves.'
                ),
                keywords='RPG, fantasy, open world, action, story-driven',
                banner='https://example.com/witcher3-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                developer='CD Projekt Red',
                publisher='CD Projekt',
                genre='Action RPG',
                is_multiplayer=False,
            ),
            Game(
                title='Minecraft',
                release_date=datetime(2011, 11, 18),
                _rating=8.9,
                view_count=35000,
                is_active=True,
                short_description='Sandbox game where players build and explore blocky worlds',
                long_description=(
                    'A sandbox video game where players can build constructions out of textured cubes in a 3D procedurally '
                    'generated world. Activities include exploration, resource gathering, crafting, and combat.'
                ),
                keywords='sandbox, creative, survival, building, exploration',
                banner='https://example.com/minecraft-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                developer='Mojang Studios',
                publisher='Mojang Studios',
                genre='Sandbox',
                is_multiplayer=True,
            ),
        ]

        video_list = [
            Video(
                title='How Computers Work',
                release_date=datetime(2023, 6, 10),
                _rating=8.7,
                view_count=15000,
                is_active=True,
                short_description='Educational video explaining computer fundamentals',
                long_description=(
                    'A comprehensive explanation of how modern computers work, from transistors and logic gates '
                    'to processors, memory, and operating systems. Perfect for beginners and enthusiasts.'
                ),
                keywords='education, computer science, technology, hardware, learning',
                banner='https://example.com/computers-banner.jpg',
                original_language_id=lang_en.id,
                age_rating_id=refs['age_ratings'][0].id,
                original_author_id=refs['authors'][0].id,
                country_id=refs['countries'][0].id,
                difficulty_level_id=refs['difficulty_levels'][0].id,
                duration_minutes=25,
                creator='Tech Explained',
            ),
        ]

        for series in series_list:
            db.add(series)
        for book in book_list:
            db.add(book)
        for film in film_list:
            db.add(film)
        for anime in anime_list:
            db.add(anime)
        for podcast in podcast_list:
            db.add(podcast)
        for course in course_list:
            db.add(course)
        for article in article_list:
            db.add(article)
        for game in game_list:
            db.add(game)
        for video in video_list:
            db.add(video)

        await db.commit()

        total = (
            len(series_list)
            + len(book_list)
            + len(film_list)
            + len(anime_list)
            + len(podcast_list)
            + len(course_list)
            + len(article_list)
            + len(game_list)
            + len(video_list)
        )

        print(f'✓ Created {len(series_list)} series')
        print(f'✓ Created {len(book_list)} books')
        print(f'✓ Created {len(film_list)} films')
        print(f'✓ Created {len(anime_list)} anime')
        print(f'✓ Created {len(podcast_list)} podcasts')
        print(f'✓ Created {len(course_list)} courses')
        print(f'✓ Created {len(article_list)} articles')
        print(f'✓ Created {len(game_list)} games')
        print(f'✓ Created {len(video_list)} videos')
        print(f'\nTotal content items: {total}')


if __name__ == '__main__':
    print('Seeding content data...')
    asyncio.run(seed_content())
    print('Done!')
