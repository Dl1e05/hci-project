import type { ApiContent, ApiContentType, ApiResponse } from '@/app/types/api';
import type { ContentCard } from '@/app/types/content';
import { mapApiContentToCard } from '@/app/lib/apiMapper';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';

type FetchParams = {
    page?: number;
    per_page?: number;
    language_level?: string;
    genre_id?: string;
    search?: string;
};

// Универсальная функция для получения контента
export async function fetchContent(
    type: ApiContentType,
    params?: FetchParams
): Promise<{ items: ContentCard[]; total: number }> {
    try {
        // Map frontend types to backend resource paths
        const resourceMap: Record<ApiContentType, string> = {
            movie: 'films',
            anime: 'animes',
            book: 'books',
            podcast: 'podcasts',
            tvshow: 'series',
            game: 'games',
        };
        const resource = resourceMap[type] || type;

        // Backend supports skip/limit instead of page/per_page
        const perPage = params?.per_page ?? 24;
        const page = params?.page ?? 1;
        const skip = Math.max(0, (page - 1) * perPage);
        const limit = perPage;

        const queryParams = new URLSearchParams();
        queryParams.set('skip', skip.toString());
        queryParams.set('limit', limit.toString());
        if (params?.language_level) queryParams.set('language_level', params.language_level);
        if (params?.genre_id) queryParams.set('genre_id', params.genre_id);
        if (params?.search) queryParams.set('search', params.search);

        const url = `${API_BASE_URL}/content/${resource}?${queryParams.toString()}`;
        console.log('📡 Fetching:', url);

        const res = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }

        const json = await res.json();
        let items: ContentCard[] = [];
        let total = 0;

        if (Array.isArray(json)) {
            // Backend returns a list directly
            items = (json as ApiContent[]).map((item) => mapApiContentToCard(item, type));
            total = items.length; // No total provided; use current batch length
        } else {
            // Fallback to paginated shape { data, total, ... }
            const data = json as ApiResponse<ApiContent>;
            items = data.data.map((item) => mapApiContentToCard(item, type));
            total = data.total ?? items.length;
        }

        console.log('✅ Loaded from API:', items.length, 'items');
        return { items, total };
    } catch (error) {
        console.error('❌ Failed to fetch content:', error);
        return { items: [], total: 0 };
    }
}

// Получение одного элемента
export async function fetchContentById(
    type: ApiContentType,
    id: string
): Promise<ContentCard | null> {
    try {
        const resourceMap: Record<ApiContentType, string> = {
            movie: 'films',
            anime: 'animes',
            book: 'books',
            podcast: 'podcasts',
            tvshow: 'series',
            game: 'games',
        };
        const resource = resourceMap[type] || type;

        const url = `${API_BASE_URL}/content/${resource}/${id}`;
        console.log('📡 Fetching:', url);

        const res = await fetch(url, {
            cache: 'no-store',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!res.ok) {
            throw new Error(`API error: ${res.status}`);
        }

        const data: ApiContent = await res.json();
        const item = mapApiContentToCard(data, type);

        console.log('✅ Loaded from API:', item.title);
        return item;

    } catch (error) {
        console.error('❌ Failed to fetch content:', error);
        return null;
    }
}

// Специфичные функции
export const fetchMovies = (params?: FetchParams) => fetchContent('movie', params);
export const fetchMovieById = (id: string) => fetchContentById('movie', id);

export const fetchAnime = (params?: FetchParams) => fetchContent('anime', params);
export const fetchAnimeById = (id: string) => fetchContentById('anime', id);

export const fetchBooks = (params?: FetchParams) => fetchContent('book', params);
export const fetchBookById = (id: string) => fetchContentById('book', id);

export const fetchPodcasts = (params?: FetchParams) => fetchContent('podcast', params);
export const fetchPodcastById = (id: string) => fetchContentById('podcast', id);

export const fetchGames = (params?: FetchParams) => fetchContent('game', params);
export const fetchGameById = (id: string) => fetchContentById('game', id);

export const fetchTVShows = (params?: FetchParams) => fetchContent('tvshow', params);
export const fetchTVShowById = (id: string) => fetchContentById('tvshow', id);

export async function fetchContentByLevel(
    level: string,
    limit: number = 4
): Promise<{ items: ContentCard[]; total: number }> {
    try {
        // Получаем контент разных типов с фильтром по уровню
        const [movies, books, games] = await Promise.all([
            fetchMovies({ language_level: level, per_page: Math.ceil(limit / 3) }),
            fetchBooks({ language_level: level, per_page: Math.ceil(limit / 3) }),
            fetchGames({ language_level: level, per_page: Math.ceil(limit / 3) }),
        ]);

        // Объединяем и берем первые 4
        const allItems = [...movies.items, ...books.items, ...games.items];
        const items = allItems.slice(0, limit);

        return { items, total: allItems.length };
    } catch (error) {
        console.error('Failed to fetch content by level:', error);
        throw error;
    }
}