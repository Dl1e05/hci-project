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
        <section className="bg-slate-700/50 rounded-3xl p-8 mb-12">
            <h2 className="text-3xl font-bold text-white mb-6">About {item.title}</h2>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Постер */}
                <div className="relative aspect-[2/3] rounded-2xl overflow-hidden bg-gray-800">
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
                <div className="lg:col-span-2 space-y-4 text-white/80">
                    {/* Мета данные */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-white/60">Genre:</span>
                            <span className="ml-2 text-white">
                                {item.genres && item.genres.length > 0 
                                    ? item.genres.join(', ') 
                                    : item.genre}
                            </span>
                        </div>
                        <div>
                            <span className="text-white/60">Year:</span>
                            <span className="ml-2 text-white">{item.year}</span>
                        </div>
                        {item.duration && (
                            <div>
                                <span className="text-white/60">Time:</span>
                                <span className="ml-2 text-white">
                                    {Math.floor(item.duration / 60)}h {item.duration % 60}m
                                </span>
                            </div>
                        )}
                        {item.country && (
                            <div>
                                <span className="text-white/60">Country:</span>
                                <span className="ml-2 text-white">{item.country}</span>
                            </div>
                        )}
                        {item.ageRatingValue && (
                            <div>
                                <span className="text-white/60">Age:</span>
                                <span className="ml-2 text-white">{item.ageRatingValue}</span>
                            </div>
                        )}
                        <div>
                            <span className="text-white/60">Language level:</span>
                            <span className="ml-2 text-white">{item.languageLevel}</span>
                        </div>
                    </div>

                    {/* Языки */}
                    {item.audioLanguages && item.audioLanguages.length > 0 && (
                        <div>
                            <span className="text-white/60 text-sm">Audio:</span>
                            <span className="ml-2 text-white text-sm">
                                {item.audioLanguages.join(', ')}
                            </span>
                        </div>
                    )}
                    {item.subtitleLanguages && item.subtitleLanguages.length > 0 && (
                        <div>
                            <span className="text-white/60 text-sm">Subtitles:</span>
                            <span className="ml-2 text-white text-sm">
                                {item.subtitleLanguages.join(', ')}
                            </span>
                        </div>
                    )}

                    {/* Рейтинг */}
                    <div className="flex items-center gap-2 pt-4">
            <span className="bg-yellow-500 text-gray-900 text-lg font-bold px-3 py-1 rounded">
              {item.rating}
            </span>
                        <span className="text-white/60 text-sm">IMDb</span>
                    </div>

                    {/* Описание */}
                    <p className="text-white/90 leading-relaxed pt-4">
                        {item.fullDescription || item.description}
                    </p>

                    {/* Кнопки */}
                    <div className="flex items-center gap-4 pt-4">
                        {watchHref ? (
                            <a href={watchHref} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-gray-900 px-6 py-2.5 rounded-lg font-semibold transition-colors">
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </a>
                        ) : (
                            <button className="flex items-center gap-2 bg-yellow-500/60 text-gray-900 px-6 py-2.5 rounded-lg font-semibold cursor-not-allowed" disabled>
                                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                                </svg>
                                Watch Now
                            </button>
                        )}
                        {previewHref ? (
                            <a href={previewHref} target="_blank" rel="noopener noreferrer" className="border border-white/30 hover:border-white/50 text-white px-6 py-2.5 rounded-lg font-semibold transition-colors">
                                Preview
                            </a>
                        ) : (
                            <button className="border border-white/20 text-white/60 px-6 py-2.5 rounded-lg font-semibold cursor-not-allowed" disabled>
                                Preview
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
}