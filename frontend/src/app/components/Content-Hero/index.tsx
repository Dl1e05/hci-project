'use client';
import React from 'react';
import Image from 'next/image';
import {ContentCard} from "@/app/types/content";

type Props = {
    item: ContentCard;
};

export default function ContentHero({ item }: Props) {
    return (
        <div className="relative h-[60vh] min-h-[500px] overflow-hidden">
            {/* Фоновое изображение */}
            <div className="absolute inset-0">
                <Image
                    src={item.imageUrl}
                    alt={item.title}
                    fill
                    className="object-cover opacity-40 blur-sm"
                    priority
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
                        <button className="flex items-center gap-2 bg-yellow-500 hover:bg-yellow-600 text-gray-900 px-6 py-3 rounded-lg font-semibold transition-colors">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                            </svg>
                            Watch Now
                        </button>
                        <button className="border-2 border-white/30 hover:border-white/50 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                            Preview
                        </button>
                    </div>

                    {/* Социальные кнопки */}
                    <div className="flex items-center gap-3 mt-6">
                        <button className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/>
                            </svg>
                        </button>
                        <button className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                            </svg>
                        </button>
                        <button className="w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors">
                            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 2C6.477 2 2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12c0-5.523-4.477-10-10-10z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}