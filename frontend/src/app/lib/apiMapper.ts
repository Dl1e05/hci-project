import type { ContentCard, ContentType } from '@/app/types/content';
import type { ApiContent, ApiContentType } from '@/app/types/api';
import { generateSlug } from './utils';

const contentTypeMap: Record<ApiContentType, ContentType> = {
    'movie': 'Movies',
    'tvshow': 'TV shows',
    'anime': 'Anime',
    'book': 'Books',
    'podcast': 'Podcasts',
    'game': 'Games',
};

export function mapApiContentToCard(apiContent: ApiContent, type: ApiContentType): ContentCard {
    return {
        id: apiContent.id,
        title: apiContent.title,
        slug: generateSlug(apiContent.title),
        year: new Date(apiContent.release_date).getFullYear(),
        rating: apiContent.rating || 0,
        description: apiContent.short_description,
        imageUrl: apiContent.poster,
        bannerUrl: apiContent.banner,
        trailerUrl: apiContent.trailer,
        genre: apiContent.genre_ids[0] || 'Unknown',
        languageLevel: 'C1', // TODO: получить с бэка
        contentType: contentTypeMap[type],
        fullDescription: apiContent.long_description,
        duration: apiContent.duration_minutes,
        director: apiContent.director,
        keywords: apiContent.keywords,
        isActive: apiContent.is_active,
        link: apiContent.link,
    };
}