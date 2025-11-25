export type ApiContentType = 'movie' | 'anime' | 'book' | 'podcast' | 'tvshow' | 'game';

// Reference types (nested objects from API)
export type ApiGenre = {
    id: string;
    name: string;
    created_at: string;
    updated_at: string;
};

export type ApiLanguage = {
    id: number;
    name: string;
    code: string;
    created_at: string;
    updated_at: string;
};

export type ApiCountry = {
    id: string;
    name: string;
    code: string;
    created_at: string;
    updated_at: string;
};

export type ApiAgeRating = {
    id: number;
    name: string;
    value: string;
    description: string;
    created_at: string;
    updated_at: string;
};

export type ApiContent = {
    id: string;
    title: string;
    release_date: string;
    is_active: boolean;
    short_description: string | null;
    long_description: string | null;
    keywords: string | null;
    banner: string | null; // Banner image URL (always present or null)
    trailer: string | null;
    link: string | null;
    poster?: string | null; // Poster image URL (optional, backend may not have this field)
    // IDs (for backward compatibility)
    original_language_id: number;
    age_rating_id: number;
    original_author_id: number;
    country_id: string;
    genre_ids?: string[]; // May not be present if genres are nested
    audio_language_ids?: number[];
    subtitle_language_ids?: number[];
    tag_ids?: string[];
    // Nested objects (if API returns relationships)
    genres?: ApiGenre[];
    audio_languages?: ApiLanguage[];
    subtitle_languages?: ApiLanguage[];
    original_language?: ApiLanguage;
    age_rating?: ApiAgeRating;
    country?: ApiCountry;
    duration_minutes: number | null;
    director?: string | null;
    rating: number;
    view_count?: number;
};

export type ApiResponse<T> = {
    data: T[];
    total: number;
    page: number;
    per_page: number;
};