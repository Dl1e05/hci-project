import React from 'react';
import Layout from '@/app/components/Layout';
import ContentGrid from '@/app/(pages)/catalog/components/Content-Grid';
import { fetchGames } from '@/app/lib/api/contentApi';

export default async function PlayPage() {
    const { items } = await fetchGames({ per_page: 24 }).catch(() => ({ items: [] } as any));
    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Play</h1>
                <ContentGrid items={items} />
            </div>
        </Layout>
    );
}