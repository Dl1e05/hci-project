import React from 'react';
import { notFound } from 'next/navigation';
import { fetchPodcastById, fetchPodcasts } from '@/app/lib/api/contentApi';
import ContentHero from '@/app/components/Content-Hero';
import AboutSection from '@/app/components/About-Section';
import SimilarContent from '@/app/components/Similar-Content';
import ReviewsSection from '@/app/components/Review-Section';
import ContentHeader from '@/app/components/Content-Header';

type Props = {
    params: { id: string };
};

export default async function ListenDetailPage({ params }: Props) {
    const item = await fetchPodcastById(params.id);
    if (!item || item.contentType !== 'Podcasts') {
        notFound();
    }

    // Fetch some similar items (same type), exclude current
    const { items: rawSimilar } = await fetchPodcasts({ per_page: 8 });
    const similarItems = rawSimilar.filter((i) => i.id !== item.id).slice(0, 8);

    return (
        <div className="min-h-screen bg-white">
            <ContentHeader />
            <ContentHero item={item} />
            <div className="container mx-auto px-6 py-12">
                <AboutSection item={item} />
                <SimilarContent items={similarItems} title={`More like ${item.title}`} />
                <ReviewsSection contentId={item.id} />
            </div>
        </div>
    );
}
