from fastapi import APIRouter

from app.auth.api.v1.jwt_router import router as jwt_router
from app.auth.api.v1.router import router as auth_router
from app.users.api.v1.router import router as users_router

# Reference routers
from app.references.api.v1.tags_router import router as tags_router
from app.references.api.v1.content_types_router import router as content_types_router
from app.references.api.v1.genres_router import router as genres_router
from app.references.api.v1.countries_router import router as countries_router
from app.references.api.v1.languages_router import router as languages_router
from app.references.api.v1.authors_router import router as authors_router
from app.references.api.v1.platforms_router import router as platforms_router
from app.references.api.v1.age_ratings_router import router as age_ratings_router
from app.references.api.v1.difficulty_levels_router import router as difficulty_levels_router
from app.references.api.v1.content_statuses_router import router as content_statuses_router
from app.references.api.v1.content_categories_router import router as content_categories_router

# Content routers
from app.content.api.v1.series_router import router as series_router
from app.content.api.v1.books_router import router as books_router
from app.content.api.v1.films_router import router as films_router
from app.content.api.v1.animes_router import router as animes_router
from app.content.api.v1.podcasts_router import router as podcasts_router
from app.content.api.v1.courses_router import router as courses_router
from app.content.api.v1.articles_router import router as articles_router
from app.content.api.v1.games_router import router as games_router
from app.content.api.v1.videos_router import router as videos_router

main_router = APIRouter()

# Auth and users
main_router.include_router(auth_router)
main_router.include_router(jwt_router)
main_router.include_router(users_router)

# Reference data
main_router.include_router(tags_router)
main_router.include_router(content_types_router)
main_router.include_router(genres_router)
main_router.include_router(countries_router)
main_router.include_router(languages_router)
main_router.include_router(authors_router)
main_router.include_router(platforms_router)
main_router.include_router(age_ratings_router)
main_router.include_router(difficulty_levels_router)
main_router.include_router(content_statuses_router)
main_router.include_router(content_categories_router)

# Content types
main_router.include_router(series_router)
main_router.include_router(books_router)
main_router.include_router(films_router)
main_router.include_router(animes_router)
main_router.include_router(podcasts_router)
main_router.include_router(courses_router)
main_router.include_router(articles_router)
main_router.include_router(games_router)
main_router.include_router(videos_router)

__all__ = ['main_router']
