'use client'
import ContentGrid from '@/app/(pages)/catalog/components/Content-Grid';
import { allContentData } from '@/app/(pages)/catalog/contentData';
import Layout from '@/app/components/Layout';

export default function AllContentPage() {
    const allItems = Object.values(allContentData).flat();

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">All Content</h1>
                <ContentGrid items={allItems} showFilters={true} />
            </div>
        </Layout>
    );
}