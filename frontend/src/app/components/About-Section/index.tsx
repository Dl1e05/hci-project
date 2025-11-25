'use client';
import React from 'react';
import Image from 'next/image';
import type { ContentCard } from '@/app/types/content';
import { getSafeImageUrl } from '@/app/lib/utils';

type Props = {
    item: ContentCard;
};

export default function AboutSection({ item }: Props) {
    const imageSrc = getSafeImageUrl(item.imageUrl);
    const watchHref = item.link ?? undefined;
    const previewHref = item.trailerUrl ?? undefined;

    return (
        <section className="bg-white rounded-3xl p-8 mb-12 shadow-sm">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">About {item.title}</h2>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Постер */}
                <div className="relative aspect-[2/3] rounded-2xl overflow-hidden bg-gray-200">
                    <Image
                        src={imageSrc}
                        alt={item.title}
                        fill
                        className="object-cover"
                        unoptimized={true}
                        sizes="(max-width: 1024px) 100vw, 33vw"
                    />
                </div>

                {/* Информация */}
                <div className="lg:col-span-2 space-y-4 text-gray-700">
                    {/* Мета данные */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-gray-500 font-medium">Genre:</span>
                            <span className="ml-2 text-gray-900">
                                {item.genres && item.genres.length > 0 
                                    ? item.genres.join(', ') 
                                    : item.genre}
                            </span>
                        </div>
                        {item.duration && (
                            <div>
                                <span className="text-gray-500 font-medium">Time:</span>
                                <span className="ml-2 text-gray-900">
                                    {Math.floor(item.duration / 60)}h {item.duration % 60}m
                                </span>
                            </div>
                        )}
                        {item.country && (
                            <div>
                                <span className="text-gray-500 font-medium">Country:</span>
                                <span className="ml-2 text-gray-900">{item.country}</span>
                            </div>
                        )}
                        {item.ageRatingValue && (
                            <div>
                                <span className="text-gray-500 font-medium">Age:</span>
                                <span className="ml-2 text-gray-900">{item.ageRatingValue}</span>
                            </div>
                        )}
                        <div>
                            <span className="text-gray-500 font-medium">Language level:</span>
                            <span className="ml-2 text-gray-900">{item.languageLevel}</span>
                        </div>
                    </div>

                    {/* Языки */}
                    {item.audioLanguages && item.audioLanguages.length > 0 && (
                        <div>
                            <span className="text-gray-500 font-medium text-sm">Audio:</span>
                            <span className="ml-2 text-gray-900 text-sm">
                                {item.audioLanguages.join(', ')}
                            </span>
                        </div>
                    )}
                    {item.subtitleLanguages && item.subtitleLanguages.length > 0 && (
                        <div>
                            <span className="text-gray-500 font-medium text-sm">Subtitles:</span>
                            <span className="ml-2 text-gray-900 text-sm">
                                {item.subtitleLanguages.join(', ')}
                            </span>
                        </div>
                    )}

                    {/* Рейтинг */}
                    <div className="flex items-center gap-2 pt-4">
                        <span className="bg-blue-500 text-white text-lg font-bold px-4 py-2 rounded">
                            {item.rating}
                        </span>
                    </div>

                    {/* Описание */}
                    <p className="text-gray-700 leading-relaxed pt-4">
                        {item.fullDescription || item.description}
                    </p>

                    {/* Кнопки */}
                    <div className="flex items-center gap-4 pt-4">
                        {watchHref ? (
                            <a href={watchHref} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 bg-blue-400 hover:bg-blue-500 text-white px-6 py-2.5 rounded-lg font-semibold transition-colors">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </a>
                        ) : (
                            <button className="flex items-center gap-2 bg-blue-400/60 text-white px-6 py-2.5 rounded-lg font-semibold cursor-not-allowed" disabled>
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </button>
                        )}
                        <button className="border-2 border-gray-300 hover:border-gray-400 text-gray-700 px-6 py-2.5 rounded-lg font-semibold transition-colors bg-white">
                            Already watched
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
}