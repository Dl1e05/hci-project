import { ContentBannerProps, ContentBanner } from '@/app/(pages)/home/components/Content-banner';
import type { ContentCard } from '@/app/types/content';

// "items" на главной приходят из API как ContentCard, но баннеру нужен href.
// Здесь вычисляем корректный href для каталога по типу и уровню.

type Props = {
    level: string;              // "A1" | "A2" | "B1" и т.д.
    items: (ContentBannerProps | ContentCard)[];
    description: string;        // Описание уровня
    badge: string;              // "Beginner" | "Elementary" | "Intermediate"
    viewMoreHref?: string;
};

function mapContentTypeToQuery(type?: ContentCard['contentType']): 'movie' | 'anime' | 'book' | 'game' | 'podcast' | 'tvshow' {
    switch (type) {
        case 'Movies':
            return 'movie';
        case 'Anime':
            return 'anime';
        case 'Books':
            return 'book';
        case 'Games':
            return 'game';
        case 'Podcasts':
            return 'podcast';
        case 'TV shows':
            return 'tvshow';
        default:
            return 'movie';
    }
}

export default function ContentBannerSection({ level, items, description, badge, viewMoreHref }: Props) {
    // Логирование для отладки
    if (typeof window === 'undefined') {
        console.log(`📦 ContentBannerSection for ${level}:`, {
            itemsCount: items.length,
            items: items.map((it: any) => ({
                id: it.id,
                title: it.title,
                contentType: (it as ContentCard).contentType,
                imageUrl: it.imageUrl || (it as ContentCard).imageUrl,
            }))
        });
    }

    // Убираем дубликаты по ID и типу контента
    const uniqueItems = items.reduce((acc, item) => {
        const contentCard = item as ContentCard;
        const existingById = acc.find((i: any) => (i as ContentCard).id === contentCard.id);
        const existingByType = acc.find((i: any) => (i as ContentCard).contentType === contentCard.contentType);
        
        // Добавляем только если нет дубликата по ID И нет дубликата по типу
        if (!existingById && !existingByType) {
            acc.push(item);
        }
        return acc;
    }, [] as (ContentBannerProps | ContentCard)[]);

    const displayItems = uniqueItems.slice(0, 4);

    return (
        <section className="w-full py-8 px-6" style={{ backgroundColor: '#F9F9F9' }}>
            <div className="max-w-7xl mx-auto">
                {/* Заголовок и кнопка */}
                <div className="mb-6 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-gray-800">{level} Level</h2>
                    {viewMoreHref && (
                        <a
                            href={viewMoreHref}
                            className="rounded-lg bg-blue-100 hover:bg-blue-200 px-6 py-2.5 text-sm font-medium text-blue-700 transition-all"
                        >
                            View More
                        </a>
                    )}
                </div>

                {/* Белый контейнер с карточками */}
                <div className="bg-white rounded-3xl p-8 shadow-sm">
                    {/* Сетка карточек */}
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-6">
                        {displayItems.length > 0 ? (
                            displayItems.map((it) => {
                                const contentCard = it as ContentCard;
                                const typeQuery = mapContentTypeToQuery(contentCard.contentType);
                                const href = (it as ContentBannerProps).href ?? `/catalog?type=${typeQuery}&level=${encodeURIComponent(level)}`;
                                const bannerItem: ContentBannerProps = {
                                    id: contentCard.id || (it as any).id,
                                    title: contentCard.title || (it as any).title || 'Untitled',
                                    category: contentCard.contentType || (it as any).category,
                                    imageUrl: contentCard.imageUrl || (it as any).imageUrl || '',
                                    href,
                                };
                                return <ContentBanner key={bannerItem.id} item={bannerItem} />;
                            })
                        ) : (
                            <div className="col-span-4 text-center text-gray-500 py-8">
                                No content available for {level} level
                            </div>
                        )}
                    </div>

                    {/* Описание и бейдж внизу */}
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between pt-4 border-t border-slate-100">
                        <p className="text-sm leading-relaxed text-slate-600 max-w-4xl">
                            {description}
                        </p>
                        <span className="inline-flex w-fit items-center rounded-full border border-slate-300 bg-slate-50 px-5 py-2 text-sm font-medium text-slate-700 whitespace-nowrap">
                            {badge}
                        </span>
                    </div>
                </div>
            </div>
        </section>
    );
}