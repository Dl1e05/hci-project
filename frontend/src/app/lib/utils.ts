import type { ContentType } from '@/app/types/content';

/**
 * Проверяет, авторизован ли пользователь, проверяя наличие токена в localStorage или sessionStorage
 */
export function isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    const accessToken = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    return !!accessToken;
}

/**
 * Выход из системы - очищает токены из localStorage и sessionStorage
 */
export function logout(): void {
    if (typeof window === 'undefined') return;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
}

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

const FALLBACK_IMAGE = 'https://placehold.co/400x600?text=No+Image';

/**
 * Validates and sanitizes an image URL, returning a fallback if invalid
 */
export function getSafeImageUrl(imageUrl: string | null | undefined): string {
    if (!imageUrl || imageUrl.trim().length === 0) {
        return FALLBACK_IMAGE;
    }

    const trimmedUrl = imageUrl.trim();

    // Validate URL format
    try {
        const url = new URL(trimmedUrl);
        // Ensure it's http or https
        if (!['http:', 'https:'].includes(url.protocol)) {
            return FALLBACK_IMAGE;
        }
        return trimmedUrl;
    } catch {
        // Invalid URL format
        return FALLBACK_IMAGE;
    }
}

/**
 * Determines if an image should be unoptimized (for external domains like R2)
 */
export function shouldUnoptimizeImage(imageUrl: string): boolean {
    if (!imageUrl) return true; // Always unoptimize if URL is invalid
    
    try {
        const url = new URL(imageUrl);
        const hostname = url.hostname;
        
        // Unoptimize for placeholder services (they often have issues with Next.js optimization)
        if (hostname.includes('placehold.co') || hostname.includes('placeholder')) {
            return true;
        }
        
        // Unoptimize for R2 domains (Cloudflare R2 storage)
        if (hostname.includes('r2.dev') || hostname.includes('r2.cloudflarestorage.com')) {
            return true;
        }
        
        // For localhost, allow Next.js to optimize (development)
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return false;
        }
        
        // For other external domains, unoptimize to avoid CORS/optimization issues
        // This is safer and ensures images load correctly
        return true;
    } catch {
        // If URL parsing fails, unoptimize to be safe
        return true;
    }
}