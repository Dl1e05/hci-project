'use client';
import React, { useState, useMemo } from 'react';
import ContentCard from './Content-Card';
import Pagination from './Pagination';
import type { ContentCard as ContentCardType, ContentType } from '@/app/types/content';

type Props = {
    items: ContentCardType[];
    itemsPerPage?: number;
    showFilters?: boolean;
};

export default function ContentGrid({ items, itemsPerPage = 24, showFilters = true }: Props) {
    const [currentPage, setCurrentPage] = useState(1);
    const [selectedLevel, setSelectedLevel] = useState<string>('All');
    const [selectedType, setSelectedType] = useState<ContentType | 'All'>('All');

    // Фильтрация
    const filteredItems = useMemo(() => {
        return items.filter((item) => {
            const levelMatch = selectedLevel === 'All' || item.languageLevel === selectedLevel;
            const typeMatch = selectedType === 'All' || item.contentType === selectedType;
            return levelMatch && typeMatch;
        });
    }, [items, selectedLevel, selectedType]);

    // Пагинация
    const totalPages = Math.ceil(filteredItems.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentItems = filteredItems.slice(startIndex, endIndex);

    // Сброс на первую страницу при изменении фильтров
    React.useEffect(() => {
        setCurrentPage(1);
    }, [selectedLevel, selectedType]);

    return (
        <div>
            {/* Фильтры сверху */}
            {showFilters && (
                <div className="flex items-center justify-end gap-4 mb-6">
                    <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Language Level</span>
                        <select
                            value={selectedLevel}
                            onChange={(e) => setSelectedLevel(e.target.value)}
                            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-500"
                        >
                            <option>All</option>
                            <option>A1</option>
                            <option>A2</option>
                            <option>B1</option>
                            <option>B2</option>
                            <option>C1</option>
                            <option>C2</option>
                        </select>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Content Type</span>
                        <select
                            value={selectedType}
                            onChange={(e) => setSelectedType(e.target.value as ContentType | 'All')}
                            className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-500"
                        >
                            <option>All</option>
                            <option>Movies</option>
                            <option>TV shows</option>
                            <option>Books</option>
                            <option>Games</option>
                        </select>
                    </div>
                </div>
            )}

            {/* Сетка карточек */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-4 gap-6">
                {currentItems.map((item) => (
                    <ContentCard key={item.id} item={item} />
                ))}
            </div>

            {/* Сообщение если нет результатов */}
            {filteredItems.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                    No items found matching your filters.
                </div>
            )}

            {/* Пагинация */}
            {totalPages > 1 && (
                <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setCurrentPage}
                />
            )}
        </div>
    );
}