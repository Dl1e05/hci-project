import React from 'react';
import { notFound } from 'next/navigation'
import { findContentBySlug, allContentData } from '@/app/(pages)/catalog/contentData';
import Header from '@/app/components/Header';
import ContentHero from '@/app/components/Content-Hero';
import AboutSection from '@/app/components/About-Section';
import SimilarContent from '@/app/components/Similar-Content';
import ReviewsSection from '@/app/components/Review-Section';

type Props = {
    params: {
        slug: string;
    };
};

export default function WatchDetailPage({ params }: Props) {
    const item = findContentBySlug(params.slug);

    if (!item) {
        notFound();
    }

    // Похожий контент (фильтруем по жанру или уровню)
    const similarItems = allContentData
        .filter(i => i.id !== item.id && (i.genre === item.genre || i.languageLevel === item.languageLevel))
        .slice(0, 4);

    return (
        <div className="min-h-screen bg-slate-800">
            {/* Header (необязательно, если есть глобальный) */}
            <Header/>

            {/* Hero секция с фоном */}
            <ContentHero item={item} />

            {/* Основной контент */}
            <div className="container mx-auto px-6 py-12">
                {/* About секция */}
                <AboutSection item={item} />

                {/* Похожий контент */}
                <SimilarContent items={similarItems} title={`More like ${item.title}`} />

                {/* Отзывы */}
                <ReviewsSection contentId={item.id} />
            </div>
        </div>
    );
}