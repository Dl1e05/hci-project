export type ContentType = 'Movies' | 'TV shows' | 'Books' | 'Games' | 'Anime' | 'Podcasts';

export type ContentCard = {
    id: string;
    title: string;
    slug: string;
    year: number;
    rating: number;
    description: string;
    imageUrl: string;
    genre: string;
    languageLevel: string;
    contentType: ContentType;

    // Дополнительные поля
    bannerUrl?: string;
    trailerUrl?: string;
    fullDescription?: string;
    duration?: number;
    director?: string;
    keywords?: string;
    isActive?: boolean;
    link?: string;
};