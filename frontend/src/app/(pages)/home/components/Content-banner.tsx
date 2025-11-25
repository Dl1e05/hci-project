'use client'
import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getSafeImageUrl } from '@/app/lib/utils';

export type ContentBannerProps = {
    id: string;
    title: string;       // Название контента (например, "Finding Nemo")
    category?: string;    // Категория (например, "Movies", "TV shows", "Books", "Games")
    imageUrl: string;    // URL с бэка
    href?: string;
};

export function ContentBanner({item}: { item: ContentBannerProps }) {
    const [imageError, setImageError] = useState(false);
    const imageSrc = getSafeImageUrl(item.imageUrl);
    const fallbackImage = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48rectIHdpZHRoPSI0MDAiIGhlaWdodD0iNjAwIiBmaWxsPSIjZTVlN2ViIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzljYTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==';

    return (
        <Link
            href={item.href ?? '#'}
            className="group relative block overflow-hidden rounded-[20px] ring-1 ring-black/5 shadow-sm transition hover:shadow-lg"
        >
            <div className="relative aspect-[9/14] w-full bg-gray-200">
                {!imageError && imageSrc ? (
                    <Image
                        src={imageSrc}
                        alt={item.title}
                        fill
                        sizes="(max-width: 1024px) 50vw, 25vw"
                        className="object-cover"
                        unoptimized={true}
                        onError={() => setImageError(true)}
                    />
                ) : (
                    <Image
                        src={fallbackImage}
                        alt={item.title}
                        fill
                        sizes="(max-width: 1024px) 50vw, 25vw"
                        className="object-cover"
                        unoptimized={true}
                    />
                )}

                {/* Категория в центре */}
                {item.category && (
                    <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
                        <span className="rounded-full bg-blue-500 px-5 py-2 text-sm font-semibold text-white backdrop-blur shadow-md">
                            {item.category}
                        </span>
                    </div>
                )}
            </div>
        </Link>
    )
}

export default ContentBanner;