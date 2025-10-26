import type { ContentBannerProps } from "@/app/(pages)/home/components/Content-banner";
import { fallbackContentBanners } from "@/app/(pages)/home/fallbackData";

export async function fetchContentBanner(): Promise<ContentBannerProps[]> {
    // Если нет API_BASE_URL, сразу возвращаем fallback данные
    if (!process.env.API_BASE_URL) {
        console.log('⚠️ API_BASE_URL not configured, using fallback data');
        return fallbackContentBanners;
    }

    try {
        const res = await fetch(`${process.env.API_BASE_URL}/content-banners`, {
            cache: 'no-store',
            // Добавляем таймаут
            signal: AbortSignal.timeout(5000), // 5 секунд таймаут
        });

        if (!res.ok) {
            console.warn('⚠️ API returned error, using fallback data');
            return fallbackContentBanners;
        }

        const data = await res.json();
        console.log('✅ Data loaded from API');
        return data;

    } catch (error) {
        console.error('❌ Failed to fetch from API:', error);
        console.log('⚠️ Using fallback data');
        return fallbackContentBanners;
    }
}