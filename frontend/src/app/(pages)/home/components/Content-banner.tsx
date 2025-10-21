'use client'
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';

export type ContentBannerProps = {
    id: string;
    title: string;       // "Movies" | "TV shows" | "Books" | "Games"
    imageUrl: string;    // URL с бэка
    href?: string;
};

export function ContentBanner({item}: { item: ContentBannerProps }) {
    return (
        <Link
            href={item.href ?? '#'}
            className="group relative block overflow-hidden rounded-[20px] ring-1 ring-black/5 shadow-sm transition hover:shadow-lg"
        >
            <div className="relative aspect-[9/14] w-full">
                <Image
                    src={item.imageUrl}
                    alt={item.title}
                    fill
                    sizes="(max-width: 1024px) 50vw, 25vw"
                    className="object-cover"
                />
            </div>

            {/* центр-пилюля */}
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
        <span className="rounded-full bg-white/95 px-5 py-2 text-sm font-semibold text-gray-900 backdrop-blur">
          {item.title}
        </span>
            </div>
        </Link>
    )
}

export default ContentBanner;