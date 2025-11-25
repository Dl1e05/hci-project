'use client';
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import type { ContentCard } from '@/app/types/content';
import { getContentUrl, getSafeImageUrl } from '@/app/lib/utils';

type Props = {
    items: ContentCard[];
    title: string;
};

export default function SimilarContent({ items, title }: Props) {
    return (
        <section className="mb-12">
            <h2 className="text-3xl font-bold text-white mb-6">{title}</h2>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {items.map((item) => {
                    const imageSrc = getSafeImageUrl(item.imageUrl);
                    return (
                        <Link key={item.id} href={getContentUrl(item)} className="group">
                            <div className="relative aspect-[2/3] rounded-xl overflow-hidden bg-gray-800">
                                <Image
                                    src={imageSrc}
                                    alt={item.title}
                                    fill
                                    className="object-cover group-hover:scale-105 transition-transform duration-300"
                                    unoptimized={true}
                                    sizes="(max-width: 768px) 50vw, 25vw"
                                />
                            </div>
                        </Link>
                    );
                })}
            </div>
        </section>
    );
}