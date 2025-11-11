'use client';
import React from 'react';
import Image from 'next/image';
import {ContentCard} from "@/app/types/content";
import { getSafeImageUrl } from '@/app/lib/utils';

type Props = {
    item: ContentCard;
};

export default function ContentHero({ item }: Props) {
    const imageSrc = getSafeImageUrl(item.bannerUrl || item.imageUrl);
    const watchHref = item.link ?? undefined;
    const previewHref = item.trailerUrl ?? undefined;

    return (
        <div className="relative h-[60vh] min-h-[500px] overflow-hidden">
            {/* Фоновое изображение */}
            <div className="absolute inset-0">
                <Image
                    src={imageSrc}
                    alt={item.title}
                    fill
                    className="object-cover opacity-40 blur-sm"
                    priority
                    unoptimized={true}
                    sizes="100vw"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-slate-900/90 to-slate-900/60" />
            </div>

            {/* Контент */}
            <div className="relative h-full container mx-auto px-6 flex items-center">
                <div className="max-w-2xl">
                    {/* Заголовок */}
                    <h1 className="text-6xl font-bold text-white mb-4 drop-shadow-lg">
                        {item.title}
                    </h1>

                    {/* Мета информация */}
                    <div className="flex items-center gap-4 mb-6 text-white/90">
                        <span className="text-sm">{item.year}</span>
                        <span className="text-sm">•</span>
                        <span className="text-sm">{item.contentType}</span>
                        <span className="flex items-center gap-1">
                          <svg className="w-5 h-5 text-yellow-400 fill-current" viewBox="0 0 20 20">
                            <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                          </svg>
                        <span className="font-semibold">{item.rating}</span>
                        </span>
                    </div>

                    {/* Кнопки */}
                    <div className="flex items-center gap-4">
                        {watchHref ? (
                            <a href={watchHref} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-gray-900 px-6 py-3 rounded-lg font-semibold transition-colors">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </a>
                        ) : (
                            <button className="flex items-center gap-2 bg-yellow-500/60 text-gray-900 px-6 py-3 rounded-lg font-semibold cursor-not-allowed" disabled>
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </button>
                        )}

                        {previewHref ? (
                            <a href={previewHref} target="_blank" rel="noopener noreferrer" className="border-2 border-white/30 hover:border-white/50 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                                Preview
                            </a>
                        ) : (
                            <button className="border-2 border-white/20 text-white/60 px-6 py-3 rounded-lg font-semibold cursor-not-allowed" disabled>
                                Preview
                            </button>
                        )}
                    </div>


                </div>
            </div>
        </div>
    );
}