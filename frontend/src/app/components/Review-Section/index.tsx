'use client';
import React, { useState } from 'react';

type Review = {
    id: string;
    author: string;
    avatar: string;
    rating: number;
    text: string;
    date: string;
    likes: number;
    dislikes: number;
};

type Props = {
    contentId: string;
};

const mockReviews: Review[] = [
    {
        id: '1',
        author: 'Margarita_25',
        avatar: 'https://placehold.co/40x40/3498db/ffffff?text=M',
        rating: 5,
        text: 'I just have seen Sense &Film of this movie while still picturing ~ It\'s so reliably picturesque and will have smiles/deals, sad comedy story. Love it!',
        date: '88 min ago',
        likes: 2,
        dislikes: 0,
    },
    {
        id: '2',
        author: 'Evgenii_Alaska',
        avatar: 'https://placehold.co/40x40/e74c3c/ffffff?text=E',
        rating: 4,
        text: 'I like the script because of the film, a good visual-crafted thing. The dialog-highlight elements give such a good visual-uplift so getting so properly.',
        date: '18 min ago',
        likes: 1,
        dislikes: 0,
    },
    {
        id: '3',
        author: 'Zhangara_da',
        avatar: 'https://placehold.co/40x40/9b59b6/ffffff?text=Z',
        rating: 5,
        text: 'A pure cinema in each cell – the visuals could charming, building, unbeatable all at once.',
        date: '9 July 2024',
        likes: 6,
        dislikes: 0,
    },
];

export default function ReviewsSection({ contentId }: Props) {
    const [reviews] = useState<Review[]>(mockReviews);
    const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest'>('newest');

    return (
        <section className="bg-slate-700/50 rounded-3xl p-8">
            <h2 className="text-3xl font-bold text-white mb-6">Reviews</h2>

            {/* Форма добавления отзыва */}
            <div className="bg-slate-600/50 rounded-2xl p-6 mb-6">
                <p className="text-white/70 text-sm mb-4">Post a comment for this series:</p>

                <textarea
                    placeholder="Review Text..."
                    className="w-full bg-slate-700/50 text-white rounded-lg p-4 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-white/40 mb-4"
                />

                <div className="flex items-center justify-between">
                    <button className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 px-6 py-2 rounded-lg font-semibold transition-colors">
                        Post comment
                    </button>
                    <div className="flex items-center gap-2 text-white/60 text-sm">
                        <span>Your rating</span>
                        <div className="flex gap-1">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <button key={star} className="text-yellow-500 hover:text-yellow-400">
                                    <svg className="w-5 h-5 fill-current" viewBox="0 0 20 20">
                                        <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                                    </svg>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>

            {/* Фильтры */}
            <div className="flex items-center gap-3 mb-6">
                <button
                    onClick={() => setSortBy('newest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        sortBy === 'newest' ? 'bg-yellow-500 text-gray-900' : 'bg-slate-600 text-white hover:bg-slate-500'
                    }`}
                >
                    Newest
                </button>
                <button
                    onClick={() => setSortBy('oldest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        sortBy === 'oldest' ? 'bg-yellow-500 text-gray-900' : 'bg-slate-600 text-white hover:bg-slate-500'
                    }`}
                >
                    Oldest
                </button>
                <button
                    onClick={() => setSortBy('highest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        sortBy === 'highest' ? 'bg-yellow-500 text-gray-900' : 'bg-slate-600 text-white hover:bg-slate-500'
                    }`}
                >
                    Highest
                </button>
                <span className="ml-auto text-white/60 text-sm">({reviews.length})</span>
            </div>

            {/* Список отзывов */}
            <div className="space-y-4">
                {reviews.map((review) => (
                    <div key={review.id} className="bg-slate-600/50 rounded-2xl p-6">
                        <div className="flex items-start gap-4">
                            {/* Аватар */}
                            <img src={review.avatar} alt={review.author} className="w-10 h-10 rounded-full" />

                            {/* Контент отзыва */}
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-3">
                                        <span className="text-white font-semibold">{review.author}</span>
                                        <span className="text-yellow-500 text-sm">{'★'.repeat(review.rating)}</span>
                                    </div>
                                    <span className="text-white/60 text-sm">{review.date}</span>
                                </div>

                                <p className="text-white/80 mb-4">{review.text}</p>

                                {/* Лайки/дизлайки */}
                                <div className="flex items-center gap-4">
                                    <button className="flex items-center gap-2 text-white/60 hover:text-white transition-colors">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                        </svg>
                                        <span className="text-sm">{review.likes}</span>
                                    </button>
                                    <button className="flex items-center gap-2 text-white/60 hover:text-white transition-colors">
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                                        </svg>
                                        <span className="text-sm">{review.dislikes}</span>
                                    </button>
                                    <button className="text-white/60 hover:text-white transition-colors text-sm ml-auto">
                                        Report
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
}