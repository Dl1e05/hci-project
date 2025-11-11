from .animes_router import router as animes_router
from .articles_router import router as articles_router
from .books_router import router as books_router
from .courses_router import router as courses_router
from .films_router import router as films_router
from .games_router import router as games_router
from .podcasts_router import router as podcasts_router
from .series_router import router as series_router
from .videos_router import router as videos_router

__all__ = [
    'series_router',
    'books_router',
    'films_router',
    'animes_router',
    'podcasts_router',
    'courses_router',
    'articles_router',
    'games_router',
    'videos_router',
]
