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
    return (
        <section className="w-full py-8 px-6" style={{ backgroundColor: '#F9F9F9' }}>
            <div className="max-w-7xl mx-auto">
                {/* Заголовок и кнопка */}
                <div className="mb-6 flex items-center justify-between">
                    <h2 className="text-2xl font-bold text-slate-700">{level}</h2>
                    {viewMoreHref && (
                        <a
                            href={viewMoreHref}
                            className="rounded-full border-2 border-slate-300 px-6 py-2.5 text-sm font-medium text-slate-700 hover:bg-white hover:border-slate-400 transition-all"
                        >
                            View More
                        </a>
                    )}
                </div>

                {/* Белый контейнер с карточками */}
                <div className="bg-white rounded-3xl p-8 shadow-sm">
                    {/* Сетка карточек */}
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-6">
                        {items.slice(0, 4).map((it) => {
                            const typeQuery = mapContentTypeToQuery((it as ContentCard).contentType as ContentCard['contentType'] | undefined);
                            const href = (it as ContentBannerProps).href ?? `/catalog?type=${typeQuery}&level=${encodeURIComponent(level)}`;
                            const bannerItem: ContentBannerProps = {
                                id: (it as any).id,
                                title: (it as any).title,
                                imageUrl: (it as any).imageUrl,
                                href,
                            };
                            return <ContentBanner key={bannerItem.id} item={bannerItem} />;
                        })}
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