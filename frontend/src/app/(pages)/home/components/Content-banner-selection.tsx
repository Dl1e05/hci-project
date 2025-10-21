import {ContentBannerProps, ContentBanner } from '@/app/(pages)/home/components/Content-banner';

type Props = {
    level: string;              // "A1 Level" | "A2 Level" | "B1 Level" и т.д.
    items: ContentBannerProps[];
    description: string;        // Описание уровня
    badge: string;             // "Beginner" | "Elementary" | "Intermediate"
    viewMoreHref?: string;
};

export default function ContentBannerSection({ level, items, description, badge, viewMoreHref }: Props) {
    return (
        <section className="w-full py-8 px-6 bg-slate-100">
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
                        {items.slice(0, 4).map((it) => (
                            <ContentBanner key={it.id} item={it} />
                        ))}
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