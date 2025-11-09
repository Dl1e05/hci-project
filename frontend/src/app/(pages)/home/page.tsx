import React from 'react';
import Layout from "@/app/components/Layout";
import Slider from '@/app/(pages)/home/components/Slider';
import ContentBannerSection from "@/app/(pages)/home/components/Content-banner-selection";
// Local fallback data removed. Keep simple metadata for headings.
const languageLevels = {
    A1: { level: 'A1', description: 'Beginner-friendly picks', badge: 'A1' },
    A2: { level: 'A2', description: 'Elementary level content', badge: 'A2' },
    B1: { level: 'B1', description: 'Intermediate selections', badge: 'B1' },
    B2: { level: 'B2', description: 'Upper-intermediate picks', badge: 'B2' },
    C1: { level: 'C1', description: 'Advanced content', badge: 'C1' },
    C2: { level: 'C2', description: 'Proficient level content', badge: 'C2' },
} as const;
import { fetchContentByLevel } from '@/app/lib/api/contentApi';

export default async function Home() {
    // Пытаемся получить данные с API для каждого уровня
    const [a1Data, a2Data, b1Data, b2Data, c1Data, c2Data] = await Promise.all([
        fetchContentByLevel('A1', 4).catch(() => ({ items: [], total: 0 })),
        fetchContentByLevel('A2', 4).catch(() => ({ items: [], total: 0 })),
        fetchContentByLevel('B1', 4).catch(() => ({ items: [], total: 0 })),
        fetchContentByLevel('B2', 4).catch(() => ({ items: [], total: 0 })),
        fetchContentByLevel('C1', 4).catch(() => ({ items: [], total: 0 })),
        fetchContentByLevel('C2', 4).catch(() => ({ items: [], total: 0 })),
    ]);

    return (
        <Layout>
            <Slider />
            <main>
                {/* A1 Level */}
                {a1Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.A1.level}
                        items={a1Data.items}
                        description={languageLevels.A1.description}
                        badge={languageLevels.A1.badge}
                        viewMoreHref="/catalog?level=A1"
                    />
                )}

                {/* A2 Level */}
                {a2Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.A2.level}
                        items={a2Data.items}
                        description={languageLevels.A2.description}
                        badge={languageLevels.A2.badge}
                        viewMoreHref="/catalog?level=A2"
                    />
                )}

                {/* B1 Level */}
                {b1Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.B1.level}
                        items={b1Data.items}
                        description={languageLevels.B1.description}
                        badge={languageLevels.B1.badge}
                        viewMoreHref="/catalog?level=B1"
                    />
                )}

                {/* B2 Level */}
                {b2Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.B2.level}
                        items={b2Data.items}
                        description={languageLevels.B2.description}
                        badge={languageLevels.B2.badge}
                        viewMoreHref="/catalog?level=B2"
                    />
                )}

                {/* C1 Level */}
                {c1Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.C1.level}
                        items={c1Data.items}
                        description={languageLevels.C1.description}
                        badge={languageLevels.C1.badge}
                        viewMoreHref="/catalog?level=C1"
                    />
                )}

                {/* C2 Level */}
                {c2Data.items.length > 0 && (
                    <ContentBannerSection
                        level={languageLevels.C2.level}
                        items={c2Data.items}
                        description={languageLevels.C2.description}
                        badge={languageLevels.C2.badge}
                        viewMoreHref="/catalog?level=C2"
                    />
                )}
            </main>
        </Layout>
    );
}