import { fetchMovies, fetchAnime, fetchBooks } from '@/app/lib/api/contentApi';
import type { ContentCard } from '@/app/types/content';

// Для главной страницы - получаем по несколько элементов каждого типа
export async function fetchHomeContent(): Promise<{
    movies: ContentCard[];
    anime: ContentCard[];
    books: ContentCard[];
}> {
    try {
        const [moviesResult, animeResult, booksResult] = await Promise.all([
            fetchMovies({ per_page: 4 }),
            fetchAnime({ per_page: 4 }),
            fetchBooks({ per_page: 4 }),
        ]);

        return {
            movies: moviesResult.items,
            anime: animeResult.items,
            books: booksResult.items,
        };
    } catch (error) {
        console.error('Failed to fetch home content:', error);
        return { movies: [], anime: [], books: [] };
    }
}