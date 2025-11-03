export type ContentType = 'Movies' | 'TV shows' | 'Books' | 'Games';

export type ContentCard = {
    id: string;
    title: string;
    slug: string; // Добавили slug
    year: number;
    rating: number;
    description: string;
    imageUrl: string;
    genre: string;
    languageLevel: string;
    contentType: ContentType;
};