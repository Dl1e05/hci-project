import React from 'react';
import { fetchMovies, fetchAnime, fetchBooks, fetchGames, fetchPodcasts } from '@/app/lib/api/contentApi';
import ContentGrid from './components/Content-Grid';
import Filters from './components/Filters';
import Layout from "@/app/components/Layout";

type SearchParams = {
    type?: 'movie' | 'anime' | 'book' | 'game' | 'podcast';
    page?: string;
    level?: string;
};

export default async function CatalogPage({
                                              searchParams,
                                          }: {
    searchParams: SearchParams;
}) {
    const type = searchParams.type || 'movie';
    const page = Number(searchParams.page) || 1;
    const level = searchParams.level;

    // Выбираем правильную функцию в зависимости от типа
    const fetchFunctions = {
        movie: fetchMovies,
        anime: fetchAnime,
        book: fetchBooks,
        game: fetchGames,
        podcast: fetchPodcasts,
    };

    const { items, total } = await fetchFunctions[type]({
        page,
        per_page: 24,
        language_level: level,
    });

    return (
        <Layout>
            <div className="container mx-auto px-6 py-8">
                <Filters />
                <ContentGrid items={items} itemsPerPage={24} showFilters={false} />
            </div>
        </Layout>
    );
}