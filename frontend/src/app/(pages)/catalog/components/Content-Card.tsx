'use client';
import React, { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import type { ContentCard } from '@/app/types/content';
import { getContentUrl, getSafeImageUrl } from '@/app/lib/utils';

type Props = {
    item: ContentCard;
};

export default function ContentCard({ item }: Props) {
    const url = getContentUrl(item);
    const [imageError, setImageError] = useState(false);
    const [imgSrc, setImgSrc] = useState(() => getSafeImageUrl(item.imageUrl));

    const handleImageError = () => {
        if (!imageError) {
            setImageError(true);
            // Try to use a simpler fallback
            setImgSrc('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48rectIHdpZHRoPSI0MDAiIGhlaWdodD0iNjAwIiBmaWxsPSIjZTVlN2ViIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzljYTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==');
        }
    };

    return (
        <Link href={url} className="group block">
            <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden">
                <div className="relative aspect-[2/3] bg-gray-200">
                    <Image
                        src={imgSrc}
                        alt={item.title}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-300"
                        onError={handleImageError}
                        unoptimized={true}
                        sizes="(max-width: 768px) 50vw, (max-width: 1024px) 33vw, 25vw"
                    />
                    <div className="absolute top-3 right-3 bg-black/80 backdrop-blur-sm text-white text-xs px-3 py-1 rounded-full">
                        {item.genre}
                    </div>
                </div>

                <div className="p-4">
                    <div className="flex items-start justify-between gap-2 mb-2">
                        <h3 className="font-semibold text-gray-900 line-clamp-1 flex-1">
                            {item.title}
                        </h3>
                        <span className="flex-shrink-0 bg-yellow-400 text-gray-900 text-xs font-bold px-2 py-1 rounded">
              {item.rating}
            </span>
                    </div>
                    <p className="text-sm text-gray-500 mb-2">{item.year}</p>
                    <p className="text-sm text-gray-600 line-clamp-2">{item.description}</p>
                </div>
            </div>
        </Link>
    );
}