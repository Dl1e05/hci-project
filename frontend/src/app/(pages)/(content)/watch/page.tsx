import React from 'react';
import Layout from '@/app/components/Layout';
import ContentGrid from '@/app/(pages)/catalog/components/Content-Grid';
import { fetchMovies } from '@/app/lib/api/contentApi';

export default async function WatchPage({
    searchParams,
}: {
    searchParams: { page?: string; level?: string };
}) {
    const page = Number(searchParams.page) || 1;
    const level = searchParams.level;

    const { items } = await fetchMovies({
        page,
        per_page: 12,
        language_level: level,
    });

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Movies</h1>
                <ContentGrid items={items} itemsPerPage={12} showFilters={false} />
            </div>
        </Layout>
    );
}