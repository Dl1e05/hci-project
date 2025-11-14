export type ContentType = 'Movies' | 'TV shows' | 'Books' | 'Games' | 'Anime' | 'Podcasts';

export type ContentCard = {
    id: string;
    title: string;
    slug: string;
    year: number;
    rating: number;
    description: string;
    imageUrl: string;
    genre: string; // First genre name or 'Unknown'
    genres?: string[]; // All genre names
    languageLevel: string;
    contentType: ContentType;

    // Дополнительные поля
    bannerUrl?: string;
    trailerUrl?: string;
    fullDescription?: string;
    duration?: number | null;
    director?: string | null;
    keywords?: string | null;
    isActive?: boolean;
    link?: string | null;
    
    // Detailed information from backend
    country?: string; // Country name
    countryCode?: string; // Country code (e.g., "US", "UK")
    ageRating?: string; // Age rating name (e.g., "12+", "PG-13")
    ageRatingValue?: string; // Age rating value
    audioLanguages?: string[]; // Audio language names
    subtitleLanguages?: string[]; // Subtitle language names
    originalLanguage?: string; // Original language name
};