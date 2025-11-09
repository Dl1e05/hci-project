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
        const queryParams = new URLSearchParams();
        if (params?.page) queryParams.set('page', params.page.toString());
        if (params?.per_page) queryParams.set('per_page', params.per_page.toString());
        if (params?.language_level) queryParams.set('language_level', params.language_level);
        if (params?.genre_id) queryParams.set('genre_id', params.genre_id);
        if (params?.search) queryParams.set('search', params.search);

        const url = `${API_BASE_URL}/content/${type}?${queryParams}`;
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

        const data: ApiResponse<ApiContent> = await res.json();
        const items = data.data.map(item => mapApiContentToCard(item, type));

        console.log('✅ Loaded from API:', items.length, 'items');
        return { items, total: data.total };

    } catch (error) {
        console.error('❌ Failed to fetch content:', error);
        // Возвращаем пустой массив или можно добавить fallback
        return { items: [], total: 0 };
    }
}

// Получение одного элемента
export async function fetchContentById(
    type: ApiContentType,
    id: string
): Promise<ContentCard | null> {
    try {
        const url = `${API_BASE_URL}/content/${type}/${id}`;
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