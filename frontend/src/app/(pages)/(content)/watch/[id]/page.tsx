import React from 'react';
import { notFound } from 'next/navigation';
import { fetchMovieById } from '@/app/lib/api/contentApi';
import ContentHero from '@/app/components/Content-Hero';
import AboutSection from '@/app/components/About-Section';
import SimilarContent from '@/app/components/Similar-Content';
import ReviewsSection from '@/app/components/Review-Section';

type Props = {
    params: { id: string };
};

export default async function WatchDetailPage({ params }: Props) {
    const item = await fetchMovieById(params.id);
    if (!item) {
        notFound();
    }

    return (
        <div className="min-h-screen bg-slate-800">
            <ContentHero item={item} />
            <div className="container mx-auto px-6 py-12">
                <AboutSection item={item} />
                <SimilarContent contentType="movie" currentId={item.id} />
                <ReviewsSection contentId={item.id} />
            </div>
        </div>
    );
}



