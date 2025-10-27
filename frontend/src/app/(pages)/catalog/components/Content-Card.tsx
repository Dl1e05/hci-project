'use client';
import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import type { ContentCard } from '@/app/types/content';

type Props = {
    item: ContentCard;
};

export default function ContentCard({ item }: Props) {
    // Определяем базовый путь в зависимости от типа контента
    const basePath = {
        'Movies': '/movies',
        'TV shows': '/tv-shows',
        'Books': '/books',
        'Games': '/games',
    }[item.contentType];

    return (
        <Link href={`${basePath}/${item.id}`} className="group block">
            <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden">
                {/* Изображение с жанром */}
                <div className="relative aspect-[2/3]">
                    <Image
                        src={item.imageUrl}
                        alt={item.title}
                        fill
                        className="object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    {/* Бейдж жанра */}
                    <div className="absolute top-3 right-3 bg-black/80 backdrop-blur-sm text-white text-xs px-3 py-1 rounded-full">
                        {item.genre}
                    </div>
                </div>

                {/* Информация */}
                <div className="p-4">
                    {/* Заголовок и рейтинг */}
                    <div className="flex items-start justify-between gap-2 mb-2">
                        <h3 className="font-semibold text-gray-900 line-clamp-1 flex-1">
                            {item.title}
                        </h3>
                        <span className="flex-shrink-0 bg-yellow-400 text-gray-900 text-xs font-bold px-2 py-1 rounded">
              {item.rating}
            </span>
                    </div>

                    {/* Год */}
                    <p className="text-sm text-gray-500 mb-2">{item.year}</p>

                    {/* Описание */}
                    <p className="text-sm text-gray-600 line-clamp-2">
                        {item.description}
                    </p>
                </div>
            </div>
        </Link>
    );
}