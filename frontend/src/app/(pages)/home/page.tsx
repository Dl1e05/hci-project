import React from 'react';
import Layout from "@/app/components/Layout";
import Slider from '@/app/(pages)/home/components/Slider'
import ContentBannerSection from "@/app/(pages)/home/components/Content-banner-selection";
import { languageLevels } from "@/app/(pages)/home/fallbackData";



export default async function Home(){
    return (
        <Layout >
            <Slider />
            <main>
                {/* A1 Level */}
                <ContentBannerSection
                    level={languageLevels.A1.level}
                    items={languageLevels.A1.content}
                    description={languageLevels.A1.description}
                    badge={languageLevels.A1.badge}
                    viewMoreHref="/levels/a1"
                />

                {/* A2 Level */}
                <ContentBannerSection
                    level={languageLevels.A2.level}
                    items={languageLevels.A2.content}
                    description={languageLevels.A2.description}
                    badge={languageLevels.A2.badge}
                    viewMoreHref="/levels/a2"
                />

                {/* B1 Level */}
                <ContentBannerSection
                    level={languageLevels.B1.level}
                    items={languageLevels.B1.content}
                    description={languageLevels.B1.description}
                    badge={languageLevels.B1.badge}
                    viewMoreHref="/levels/b1"
                />

                {/* B2 Level */}
                <ContentBannerSection
                    level={languageLevels.B2.level}
                    items={languageLevels.B2.content}
                    description={languageLevels.B2.description}
                    badge={languageLevels.B2.badge}
                    viewMoreHref="/levels/b2"
                />

                {/* C1 Level */}
                <ContentBannerSection
                    level={languageLevels.C1.level}
                    items={languageLevels.C1.content}
                    description={languageLevels.C1.description}
                    badge={languageLevels.C1.badge}
                    viewMoreHref="/levels/c1"
                />

                {/* C2 Level */}
                <ContentBannerSection
                    level={languageLevels.C2.level}
                    items={languageLevels.C2.content}
                    description={languageLevels.C2.description}
                    badge={languageLevels.C2.badge}
                    viewMoreHref="/levels/c2"
                />
            </main>
        </Layout>

    )
}