'use client';
import React from 'react';
import { useRouter, useSearchParams } from 'next/navigation';

const levels = ['A1','A2','B1','B2','C1','C2'] as const;
const types = [
  { key: 'movie', label: 'Movies' },
  { key: 'anime', label: 'Anime' },
  { key: 'book', label: 'Books' },
  { key: 'podcast', label: 'Podcasts' },
  { key: 'game', label: 'Games' }
] as const;

export default function Filters() {
  const router = useRouter();
  const search = useSearchParams();
  const type = search.get('type') || 'movie';
  const level = search.get('level') || '';

  function setParam(name: string, value: string) {
    const params = new URLSearchParams(search.toString());
    if (value) params.set(name, value); else params.delete(name);
    params.set('page', '1');
    router.push(`/catalog?${params}`);
  }

  return (
    <div className="flex flex-wrap gap-3 items-center mb-6">
      <div className="flex gap-2 bg-white rounded-full px-2 py-1 shadow-sm">
        {types.map(t => (
          <button
            key={t.key}
            className={`px-3 py-1 text-sm rounded-full ${type===t.key? 'bg-slate-900 text-white':'text-slate-700 hover:bg-slate-100'}`}
            onClick={() => setParam('type', t.key)}
          >{t.label}</button>
        ))}
      </div>

      <div className="flex items-center gap-2 ml-auto">
        <span className="text-sm text-slate-600">Language level</span>
        <select
          value={level}
          onChange={(e)=> setParam('level', e.target.value)}
          className="px-3 py-1 rounded-lg border border-slate-300 text-sm"
        >
          <option value="">All</option>
          {levels.map(l=> <option key={l} value={l}>{l}</option>)}
        </select>
      </div>
    </div>
  );
}



