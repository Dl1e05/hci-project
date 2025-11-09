export type ApiContentType = 'movie' | 'anime' | 'book' | 'podcast' | 'tvshow' | 'game';

export type ApiContent = {
    id: string;
    title: string;
    release_date: string;
    is_active: boolean;
    short_description: string;
    long_description: string;
    keywords: string;
    banner: string;
    trailer: string;
    link: string;
    poster: string;
    original_language_id: number;
    age_rating_id: number;
    original_author_id: number;
    country_id: string;
    genre_ids: string[];
    audio_language_ids: number[];
    subtitle_language_ids: number[];
    tag_ids: string[];
    duration_minutes: number;
    director?: string;
    rating?: number;
};

export type ApiResponse<T> = {
    data: T[];
    total: number;
    page: number;
    per_page: number;
};