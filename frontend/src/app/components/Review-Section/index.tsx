'use client';
import React, { useEffect, useMemo, useState } from 'react';

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
    const [reviews, setReviews] = useState<Review[]>([]);
    const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'highest'>('newest');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [newText, setNewText] = useState('');
    const [newRating, setNewRating] = useState<number>(0);
    const [submitting, setSubmitting] = useState(false);

    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8001';
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
        <section className="bg-slate-700/50 rounded-3xl p-8">
            <h2 className="text-3xl font-bold text-white mb-6">Reviews</h2>

            {/* Форма добавления отзыва */}
            <div className="bg-slate-600/50 rounded-2xl p-6 mb-6">
                <p className="text-white/70 text-sm mb-4">Post a comment for this series:</p>

                <textarea
                    value={newText}
                    onChange={(e) => setNewText(e.target.value)}
                    placeholder="Review Text..."
                    className="w-full bg-slate-700/50 text-white rounded-lg p-4 min-h-[120px] focus:outline-none focus:ring-2 focus:ring-yellow-500 placeholder-white/40 mb-4"
                />

                <div className="flex items-center justify-between">
                    <button
                        onClick={handleSubmit}
                        disabled={submitting || !newText.trim()}
                        className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
                            submitting || !newText.trim() ? 'bg-yellow-500/60 text-gray-900 cursor-not-allowed' : 'bg-yellow-500 hover:bg-yellow-600 text-gray-900'
                        }`}
                    >
                        {submitting ? 'Posting...' : 'Post comment'}
                    </button>
                    <div className="flex items-center gap-2 text-white/60 text-sm">
                        <span>Your rating</span>
                        <div className="flex gap-1">
                            {[1, 2, 3, 4, 5].map((star) => (
                                <button
                                    key={star}
                                    onClick={() => setNewRating(star)}
                                    type="button"
                                    className={star <= newRating ? 'text-yellow-500' : 'text-white/30 hover:text-yellow-400'}
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
                    <p className="text-red-400 text-sm mt-3">{error}</p>
                )}
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
                {loading && (
                    <div className="text-white/70">Loading comments...</div>
                )}
                {!loading && sorted.length === 0 && !error && (
                    <div className="text-white/50">No comments yet. Be the first to comment.</div>
                )}
                {!loading && sorted.map((review) => (
                    <div key={review.id} className="bg-slate-600/50 rounded-2xl p-6">
                        <div className="flex items-start gap-4">
                            {/* Аватар */}
                            {review.avatar ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img src={review.avatar} alt={review.author} className="w-10 h-10 rounded-full" />
                            ) : (
                                <div className="w-10 h-10 rounded-full bg-slate-500 flex items-center justify-center text-white/80">
                                    {review.author?.[0]?.toUpperCase() ?? '?'}
                                </div>
                            )}

                            {/* Контент отзыва */}
                            <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-3">
                                        <span className="text-white font-semibold">{review.author}</span>
                                        <span className="text-yellow-500 text-sm">{'★'.repeat(review.rating || 0)}</span>
                                    </div>
                                    <span className="text-white/60 text-sm">{new Date(review.created_at).toLocaleString()}</span>
                                </div>

                                <p className="text-white/80 mb-4">{review.text}</p>

                                {/* Лайки/дизлайки */}
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => { /* TODO: integrate like endpoint */ }}
                                        className="flex items-center gap-2 text-white/60 hover:text-white transition-colors"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
                                        </svg>
                                        <span className="text-sm">{review.likes ?? 0}</span>
                                    </button>
                                    <button
                                        onClick={() => { /* TODO: integrate dislike endpoint */ }}
                                        className="flex items-center gap-2 text-white/60 hover:text-white transition-colors"
                                    >
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14H5.236a2 2 0 01-1.789-2.894l3.5-7A2 2 0 018.736 3h4.018a2 2 0 01.485.06l3.76.94m-7 10v5a2 2 0 002 2h.096c.5 0 .905-.405.905-.904 0-.715.211-1.413.608-2.008L17 13V4m-7 10h2m5-10h2a2 2 0 012 2v6a2 2 0 01-2 2h-2.5" />
                                        </svg>
                                        <span className="text-sm">{review.dislikes ?? 0}</span>
                                    </button>
                                    <button
                                        onClick={() => { /* TODO: integrate report endpoint */ }}
                                        className="text-white/60 hover:text-white transition-colors text-sm ml-auto"
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