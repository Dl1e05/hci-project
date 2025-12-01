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
    
    const duration = item.duration ? `${Math.floor(item.duration / 60)}h ${item.duration % 60}m` : null;

    return (
        <div className="relative h-[70vh] min-h-[600px] overflow-hidden pt-16">
            {/* Фоновое изображение */}
            <div className="absolute inset-0">
                <Image
                    src={imageSrc}
                    alt={item.title}
                    fill
                    className="object-cover"
                    priority
                    unoptimized={true}
                    sizes="100vw"
                />
                <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent" />
            </div>

            {/* Контент */}
            <div className="relative h-full container mx-auto px-6 flex items-center">
                <div className="w-full flex items-end justify-between">
                    {/* Левая часть: Заголовок и кнопки */}
                    <div className="flex-1 max-w-2xl">
                        {/* Заголовок - золотистый цвет */}
                        <h1 className="text-7xl font-bold text-yellow-400 mb-6 drop-shadow-lg tracking-tight">
                            {item.title.toUpperCase()}
                        </h1>

                        {/* Кнопки */}
                        <div className="flex items-center gap-4">
                            {watchHref ? (
                                <a 
                                    href={watchHref} 
                                    target="_blank" 
                                    rel="noopener noreferrer" 
                                    className="flex items-center gap-2 bg-blue-400 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold transition-colors shadow-lg"
                                >
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                    </svg>
                                    Watch Now
                                </a>
                            ) : (
                                <button className="flex items-center gap-2 bg-blue-400/60 text-white px-6 py-3 rounded-lg font-semibold cursor-not-allowed" disabled>
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                    </svg>
                                    Watch Now
                                </button>
                            )}

                            <button className="border-2 border-white/30 hover:border-white/50 text-white px-6 py-3 rounded-lg font-semibold transition-colors bg-white/10 backdrop-blur-sm">
                                Already watched
                            </button>
                        </div>
                    </div>

                    {/* Правая часть: Мета информация */}
                    <div className="flex flex-col items-end gap-4 text-white">
                        <div className="flex flex-col items-end">
                            <span className="text-2xl font-bold">{item.title}</span>
                            <div className="flex items-center gap-2 mt-1 text-sm">
                                {duration && <span>{duration}</span>}
                                {duration && <span>-</span>}
                                <span>{item.year}</span>
                                {item.country && (
                                    <>
                                        <span>-</span>
                                        <span>{item.country}</span>
                                    </>
                                )}
                            </div>
                        </div>
                        
                        {/* Рейтинг звездами */}
                        <div className="flex items-center gap-1">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <svg 
                                    key={star} 
                                    className="w-6 h-6 text-white fill-current" 
                                    viewBox="0 0 20 20"
                                >
                                    <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                                </svg>
                            ))}
                        </div>

                        {/* Иконки действий */}
                        <div className="flex items-center gap-3">
                            <button className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/50 transition-colors">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                                </svg>
                            </button>
                            <button className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/50 transition-colors">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                </svg>
                            </button>
                            <button className="w-10 h-10 rounded-full bg-black/30 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/50 transition-colors">
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}