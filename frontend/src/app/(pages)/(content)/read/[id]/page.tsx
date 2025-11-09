import React from 'react';
import { notFound } from 'next/navigation';
import Layout from '@/app/components/Layout';
import Image from 'next/image';
import { fetchBookById } from '@/app/lib/api/contentApi';

type Props = {
    params: { id: string };
};

export default async function ReadDetailPage({ params }: Props) {
    const item = await fetchBookById(params.id);
    if (!item || item.contentType !== 'Books') {
        notFound();
    }

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="relative aspect-[2/3] rounded-2xl overflow-hidden">
                        <Image src={item.imageUrl} alt={item.title} fill className="object-cover" />
                    </div>
                    <div>
                        <h1 className="text-4xl font-bold text-gray-900 mb-4">{item.title}</h1>
                        <div className="flex items-center gap-4 mb-6">
                            <span className="bg-yellow-400 text-gray-900 text-lg font-bold px-3 py-1 rounded">{item.rating}</span>
                            <span className="text-gray-600">{item.year}</span>
                            <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm">{item.genre}</span>
                            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">{item.languageLevel}</span>
                        </div>
                        <p className="text-gray-700 text-lg leading-relaxed mb-8">{item.description}</p>
                        <button className="bg-slate-700 hover:bg-slate-800 text-white px-8 py-3 rounded-lg font-semibold transition-colors">Start Reading</button>
                    </div>
                </div>
            </div>
        </Layout>
    );
}



