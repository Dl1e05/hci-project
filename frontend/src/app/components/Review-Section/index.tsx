'use client';
import React, { useEffect, useMemo, useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/app/lib/utils';

type Review = {
    id: string;
    author: string;
    avatar?: string | null;
    rating: number;
    text: string;
    created_at: string; // ISO date from backend
    likes?: number;
    dislikes?: number;
};

type Props = {
    contentId: string;
};

export default function ReviewsSection({ contentId }: Props) {
    const router = useRouter();
    const [reviews, setReviews] = useState<Review[]>([]);
    const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest'>('newest');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [newText, setNewText] = useState('');
    const [newRating, setNewRating] = useState<number>(0);
    const [submitting, setSubmitting] = useState(false);
    const [containsSpoilers, setContainsSpoilers] = useState(false);

    const checkAuthAndRedirect = () => {
        if (!isAuthenticated()) {
            router.replace('/login');
            return false;
        }
        return true;
    };

    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const COMMENTS_PATH = process.env.NEXT_PUBLIC_COMMENTS_PATH || '/comments'; // allows switching to any backend path later

    const commentsUrl = useMemo(() => {
        const url = new URL(API_BASE_URL);
        // Ensure trailing slash behavior
        const base = url.toString().replace(/\/$/, '');
        const path = COMMENTS_PATH.startsWith('/') ? COMMENTS_PATH : `/${COMMENTS_PATH}`;
        return `${base}${path}?content_id=${encodeURIComponent(contentId)}`;
    }, [API_BASE_URL, COMMENTS_PATH, contentId]);

    useEffect(() => {
        let isCancelled = false;
        async function load() {
            setLoading(true);
            setError(null);
            try {
                const res = await fetch(commentsUrl, { cache: 'no-store' });
                if (!res.ok) throw new Error(`Failed to load comments: ${res.status}`);
                const data = await res.json();
                // Support array or envelope { data: [] }
                const list: any[] = Array.isArray(data) ? data : (data?.data ?? []);
                const mapped: Review[] = list.map((c: any) => ({
                    id: String(c.id ?? crypto.randomUUID()),
                    author: c.author ?? c.user_name ?? 'Anonymous',
                    avatar: c.avatar ?? c.user_avatar ?? null,
                    rating: Number(c.rating ?? 0),
                    text: String(c.text ?? c.comment ?? ''),
                    created_at: c.created_at ?? c.date ?? new Date().toISOString(),
                    likes: Number(c.likes ?? 0),
                    dislikes: Number(c.dislikes ?? 0),
                }));
                if (!isCancelled) setReviews(mapped);
            } catch (e: any) {
                if (!isCancelled) setError(e.message || 'Unknown error');
            } finally {
                if (!isCancelled) setLoading(false);
            }
        }
        load();
        return () => {
            isCancelled = true;
        };
    }, [commentsUrl]);

    const sorted = useMemo(() => {
        const copy = [...reviews];
        if (sortBy === 'newest') copy.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        if (sortBy === 'oldest') copy.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        if (sortBy === 'highest') copy.sort((a, b) => (b.rating || 0) - (a.rating || 0));
        return copy;
    }, [reviews, sortBy]);

    async function handleSubmit() {
        if (!checkAuthAndRedirect()) return;
        if (!newText.trim()) return;
        if (submitting) return;
        setSubmitting(true);
        setError(null);
        try {
            const payload = {
                content_id: contentId,
                text: newText.trim(),
                rating: newRating || null,
            };
            const res = await fetch(commentsUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!res.ok) throw new Error(`Failed to post comment: ${res.status}`);
            // Accept either created comment or empty body
            let created: any = null;
            try { created = await res.json(); } catch { created = null; }
            const newReview: Review = created ? {
                id: String(created.id ?? crypto.randomUUID()),
                author: created.author ?? created.user_name ?? 'You',
                avatar: created.avatar ?? created.user_avatar ?? null,
                rating: Number(created.rating ?? newRating || 0),
                text: String(created.text ?? created.comment ?? newText.trim()),
                created_at: created.created_at ?? new Date().toISOString(),
                likes: Number(created.likes ?? 0),
                dislikes: Number(created.dislikes ?? 0),
            } : {
                id: crypto.randomUUID(),
                author: 'You',
                avatar: null,
                rating: newRating || 0,
                text: newText.trim(),
                created_at: new Date().toISOString(),
                likes: 0,
                dislikes: 0,
            };
            setReviews((prev) => [newReview, ...prev]);
            setNewText('');
            setNewRating(0);
        } catch (e: any) {
            setError(e.message || 'Failed to post comment');
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <section className="bg-white rounded-3xl p-8 shadow-sm">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Reviews</h2>

            {/* Форма добавления отзыва */}
            <div className="bg-gray-100 rounded-2xl p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-gray-900 font-medium">Post a comment for this series:</h3>
                    <label className="flex items-center gap-2 text-gray-700 text-sm cursor-pointer">
                        <span>Contains spoilers</span>
                        <div className="relative">
                            <input 
                                type="checkbox" 
                                checked={containsSpoilers}
                                onChange={(e) => {
                                    if (!checkAuthAndRedirect()) return;
                                    setContainsSpoilers(e.target.checked);
                                }}
                                className="sr-only"
                            />
                            <div className={`w-11 h-6 rounded-full transition-colors ${
                                containsSpoilers ? 'bg-blue-500' : 'bg-gray-300'
                            }`}>
                                <div className={`w-5 h-5 bg-white rounded-full transition-transform mt-0.5 ml-0.5 ${
                                    containsSpoilers ? 'translate-x-5' : 'translate-x-0'
                                }`} />
                            </div>
                        </div>
                    </label>
                </div>
                
                <div className="relative mb-4">
                    <textarea
                        value={newText}
                        onChange={(e) => {
                            if (!isAuthenticated()) {
                                router.replace('/login');
                                return;
                            }
                            setNewText(e.target.value);
                        }}
                        onFocus={() => {
                            if (!isAuthenticated()) {
                                router.replace('/login');
                            }
                        }}
                        placeholder="Review Text..."
                        className="w-full bg-white text-gray-900 rounded-lg p-4 pr-12 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-300 placeholder-gray-400"
                    />
                    <div className="absolute right-4 top-4">
                        <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                        </svg>
                    </div>
                </div>

                <div className="flex items-center justify-between">
                    <button
                        onClick={handleSubmit}
                        disabled={submitting || !newText.trim()}
                        className={`flex items-center gap-2 px-6 py-2 rounded-lg font-semibold transition-colors ${
                            submitting || !newText.trim() ? 'bg-blue-400/60 text-white cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600 text-white'
                        }`}
                    >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        {submitting ? 'Submitting...' : 'Submit Review'}
                    </button>
                    <div className="flex items-center gap-2 text-gray-700 text-sm">
                        <span>Your Score</span>
                        <div className="flex gap-1">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <button
                                    key={star}
                                    onClick={() => {
                                        if (!checkAuthAndRedirect()) return;
                                        setNewRating(star);
                                    }}
                                    type="button"
                                    className={star <= newRating ? 'text-blue-500' : 'text-gray-300 hover:text-blue-400'}
                                    aria-label={`Rate ${star}`}
                                >
                                    <svg className="w-5 h-5 fill-current" viewBox="0 0 20 20">
                                        <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                                    </svg>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {error && (
                    <p className="text-red-500 text-sm mt-3">{error}</p>
                )}
            </div>

            {/* Фильтры */}
            <div className="flex items-center gap-3 mb-6">
                <span className="text-gray-700 text-sm font-medium">Sort By:</span>
                <button
                    onClick={() => setSortBy('newest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                        sortBy === 'newest' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                >
                    Newest
                </button>
                <button
                    onClick={() => setSortBy('oldest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                        sortBy === 'oldest' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                >
                    Oldest
                </button>
                <button
                    onClick={() => setSortBy('highest')}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                        sortBy === 'highest' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                >
                    Hottest
                </button>
            </div>

            {/* Список отзывов */}
            <div className="space-y-4">
                {loading && (
                    <div className="text-gray-500">Loading comments...</div>
                )}
                {!loading && sorted.length === 0 && !error && (
                    <div className="text-gray-400">No comments yet. Be the first to comment.</div>
                )}
                {!loading && sorted.map((review) => (
                    <div key={review.id} className="bg-gray-100 rounded-2xl p-6">
                        <div className="flex items-start gap-4">
                            {/* Аватар */}
                            {review.avatar ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img src={review.avatar} alt={review.author} className="w-10 h-10 rounded-full" />
                            ) : (
                                <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-gray-600 font-semibold">
                                    {review.author?.[0]?.toUpperCase() ?? '?'}
                                </div>
                            )}

                            {/* Контент отзыва */}
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-3">
                                        <span className="text-gray-900 font-semibold">{review.author}</span>
                                        {review.rating > 0 && (
                                            <span className="text-gray-600 text-sm">Score: {review.rating}/10</span>
                                        )}
                                    </div>
                                    <span className="text-gray-500 text-sm">{new Date(review.created_at).toLocaleString()}</span>
                                </div>

                                <p className="text-gray-700 mb-4">{review.text}</p>

                                {/* Лайки/дизлайки */}
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => {
                                            if (!checkAuthAndRedirect()) return;
                                            /* TODO: integrate like endpoint */
                                        }}
                                        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                        </svg>
                                        <span className="text-sm">{review.likes ?? 0}</span>
                                    </button>
                                    <button
                                        onClick={() => {
                                            if (!checkAuthAndRedirect()) return;
                                            /* TODO: integrate dislike endpoint */
                                        }}
                                        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                                        </svg>
                                        <span className="text-sm">{review.dislikes ?? 0}</span>
                                    </button>
                                    <button
                                        onClick={() => {
                                            if (!checkAuthAndRedirect()) return;
                                        }}
                                        className="text-gray-600 hover:text-gray-900 transition-colors text-sm"
                                    >
                                        Reply
                                    </button>
                                    <button
                                        onClick={() => {
                                            if (!checkAuthAndRedirect()) return;
                                            /* TODO: integrate report endpoint */
                                        }}
                                        className="text-gray-600 hover:text-gray-900 transition-colors text-sm ml-auto"
                                    >
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