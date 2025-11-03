'use client';
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import type { ContentCard } from '@/app/types/content';
import { getContentUrl } from '@/app/lib/utils';

type Props = {
    items: ContentCard[];
    title: string;
};

export default function SimilarContent({ items, title }: Props) {
    return (
        <section className="mb-12">
            <h2 className="text-3xl font-bold text-white mb-6">{title}</h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {items.map((item) => (
                    <Link key={item.id} href={getContentUrl(item)} className="group">
                        <div className="relative aspect-[2/3] rounded-xl overflow-hidden">
                            <Image
                                src={item.imageUrl}
                                alt={item.title}
                                fill
                                className="object-cover group-hover:scale-105 transition-transform duration-300"
                            />
                        </div>
                    </Link>
                ))}
            </div>
        </section>
    );
}