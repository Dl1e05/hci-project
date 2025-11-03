import React from 'react';
import Layout from '@/app/components/Layout';
import ContentGrid from '@/app/(pages)/catalog/components/Content-Grid';
import { moviesData } from '@/app/(pages)/catalog/contentData';

export default function WatchPage() {
    // Фильмы + сериалы
    const watchContent = moviesData; // moviesData + tvShowsData

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Watch</h1>
                <ContentGrid items={watchContent} />
            </div>
        </Layout>
    );
}