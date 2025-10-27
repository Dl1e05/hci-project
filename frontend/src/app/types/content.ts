export type ContentType = 'Movies' | 'TV shows' | 'Books' | 'Games';

export type ContentCard = {
    id: string;
    title: string;
    year: number;
    rating: number;
    description: string;
    imageUrl: string;
    genre: string;
    languageLevel: string;
    contentType: ContentType;
};