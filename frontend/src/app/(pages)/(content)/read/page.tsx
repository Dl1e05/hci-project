import React from 'react';
import Layout from '@/app/components/Layout';
import ContentGrid from '@/app/(pages)/catalog/components/Content-Grid';
import { booksData } from '@/app/(pages)/catalog/contentData';

export default function ReadPage() {
    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Read</h1>
                <ContentGrid items={booksData} />
            </div>
        </Layout>
    );
}