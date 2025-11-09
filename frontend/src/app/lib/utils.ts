import type { ContentType } from '@/app/types/content';

export function generateSlug(title: string): string {
    return title
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/--+/g, '-')
        .trim();
}

export function getContentAction(contentType: ContentType): string {
    const actions: Record<ContentType, string> = {
        'Movies': 'watch',
        'TV shows': 'watch',
        'Anime': 'watch',
        'Books': 'read',
        'Podcasts': 'listen',
        'Games': 'play',
    };
    return actions[contentType];
}

export function getContentUrl(item: { id: string; title: string; contentType: ContentType }): string {
    const action = getContentAction(item.contentType);
    return `/${action}/${item.id}`;
}