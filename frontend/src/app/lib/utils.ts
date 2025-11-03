import type { ContentType } from '@/app/types/content';

// Генерация slug из названия
export function generateSlug(title: string): string {
    return title
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/--+/g, '-')
        .trim();
}

// Получить действие по типу контента
export function getContentAction(contentType: ContentType): string {
    const actions = {
        'Movies': 'watch',
        'TV shows': 'watch',
        'Books': 'read',
        'Games': 'play',
    };
    return actions[contentType];
}

// Генерация URL для контента
export function getContentUrl(item: { title: string; contentType: ContentType }): string {
    const action = getContentAction(item.contentType);
    const slug = generateSlug(item.title);
    return `/${action}/${slug}`;
}

// Определить тип контента по action
export function getContentTypeByAction(action: string): ContentType | null {
    const mapping: Record<string, ContentType> = {
        'watch': 'Movies', // По умолчанию для watch
        'read': 'Books',
        'play': 'Games',
    };
    return mapping[action] || null;
}
