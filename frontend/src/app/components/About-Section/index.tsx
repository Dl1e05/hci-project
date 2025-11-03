'use client';
import React from 'react';
import Image from 'next/image';
import type { ContentCard } from '@/app/types/content';

type Props = {
    item: ContentCard;
};

export default function AboutSection({ item }: Props) {
    return (
        <section className="bg-slate-700/50 rounded-3xl p-8 mb-12">
            <h2 className="text-3xl font-bold text-white mb-6">About {item.title}</h2>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Постер */}
                <div className="relative aspect-[2/3] rounded-2xl overflow-hidden">
                    <Image
                        src={item.imageUrl}
                        alt={item.title}
                        fill
                        className="object-cover"
                    />
                </div>

                {/* Информация */}
                <div className="lg:col-span-2 space-y-4 text-white/80">
                    {/* Мета данные */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-white/60">Genre:</span>
                            <span className="ml-2 text-white">{item.genre}</span>
                        </div>
                        <div>
                            <span className="text-white/60">Year:</span>
                            <span className="ml-2 text-white">{item.year}</span>
                        </div>
                        <div>
                            <span className="text-white/60">Country:</span>
                            <span className="ml-2 text-white">UK</span>
                        </div>
                        <div>
                            <span className="text-white/60">Age:</span>
                            <span className="ml-2 text-white">12+</span>
                        </div>
                        <div>
                            <span className="text-white/60">Language level:</span>
                            <span className="ml-2 text-white">{item.languageLevel}</span>
                        </div>
                    </div>

                    {/* Языки */}
                    <div>
                        <span className="text-white/60 text-sm">Audio:</span>
                        <span className="ml-2 text-white text-sm">English</span>
                    </div>
                    <div>
                        <span className="text-white/60 text-sm">Subtitles:</span>
                        <span className="ml-2 text-white text-sm">English, Russian</span>
                    </div>

                    {/* Рейтинг */}
                    <div className="flex items-center gap-2 pt-4">
            <span className="bg-yellow-500 text-gray-900 text-lg font-bold px-3 py-1 rounded">
              {item.rating}
            </span>
                        <span className="text-white/60 text-sm">IMDb</span>
                    </div>

                    {/* Описание */}
                    <p className="text-white/90 leading-relaxed pt-4">
                        {item.description}
                    </p>

                    {/* Кнопки */}
                    <div className="flex items-center gap-4 pt-4">
                        <button className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-gray-900 px-6 py-2.5 rounded-lg font-semibold transition-colors">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                            </svg>
                            Watch Now
                        </button>
                        <button className="border border-white/30 hover:border-white/50 text-white px-6 py-2.5 rounded-lg font-semibold transition-colors">
                            Preview
                        </button>
                    </div>
                </div>
            </div>
        </section>
    );
}