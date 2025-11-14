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
    // Safe parsing of year from release_date
    let year = new Date(apiContent.release_date).getFullYear();
    if (!year || isNaN(year)) {
        year = new Date().getFullYear();
    }

    // Extract genres - check if nested objects are available (Pydantic may auto-serialize relationships)
    // If API returns nested objects, use them; otherwise we'll have to work with IDs or empty
    let genres: string[] = [];
    if (apiContent.genres && apiContent.genres.length > 0) {
        // Nested objects are available (e.g., if Pydantic auto-serializes relationships)
        genres = apiContent.genres.map(g => g.name);
    }
    // Note: If only genre_ids are available, we can't get names without additional API calls
    // So we'll just show 'Unknown' for genre in that case
    const genre = genres.length > 0 ? genres[0] : 'Unknown';

    // Extract country - check if nested object is available
    const country = apiContent.country?.name;
    const countryCode = apiContent.country?.code;

    // Extract age rating - check if nested object is available
    const ageRating = apiContent.age_rating?.name;
    const ageRatingValue = apiContent.age_rating?.value;

    // Extract languages - check if nested objects are available
    const audioLanguages = apiContent.audio_languages?.map(l => l.name) || [];
    const subtitleLanguages = apiContent.subtitle_languages?.map(l => l.name) || [];
    const originalLanguage = apiContent.original_language?.name;

    // Backend only has 'banner' field, no 'poster' field
    // Use banner for both poster (imageUrl) and banner (bannerUrl)
    // If poster exists in the future, it will take priority
    const bannerUrl = apiContent.banner || '';
    // For poster: use poster if available, otherwise fallback to banner
    // This allows backend to have separate poster field in the future
    const posterUrl = (apiContent.poster && apiContent.poster.trim()) 
        ? apiContent.poster 
        : bannerUrl; // Use banner as fallback for poster (since backend only has banner)

    return {
        id: apiContent.id,
        title: apiContent.title,
        slug: generateSlug(apiContent.title || String(apiContent.id)),
        year,
        rating: apiContent.rating ?? 0,
        description: apiContent.short_description || '',
        imageUrl: posterUrl, // Use poster if available, otherwise use banner
        bannerUrl: bannerUrl, // Banner URL (same as imageUrl if poster doesn't exist)
        trailerUrl: apiContent.trailer || '',
        genre,
        genres: genres.length > 0 ? genres : undefined,
        languageLevel: 'C1', // TODO: получить с бэка (может быть в tags или отдельном поле)
        contentType: contentTypeMap[type],
        fullDescription: apiContent.long_description || '',
        duration: apiContent.duration_minutes ?? null,
        director: apiContent.director ?? null,
        keywords: apiContent.keywords ?? null,
        isActive: apiContent.is_active,
        link: apiContent.link ?? null,
        // Detailed information
        country,
        countryCode,
        ageRating,
        ageRatingValue,
        audioLanguages: audioLanguages.length > 0 ? audioLanguages : undefined,
        subtitleLanguages: subtitleLanguages.length > 0 ? subtitleLanguages : undefined,
        originalLanguage,
    };
}