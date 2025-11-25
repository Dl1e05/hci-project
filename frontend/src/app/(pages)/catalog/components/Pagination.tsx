
import React from 'react';

type Props = {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void | Promise<void>;
};

export default function Pagination({ currentPage, totalPages, onPageChange }: Props) {
    const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

    return (
        <div className="flex justify-center items-center gap-2 py-8">
            <div className="flex items-center gap-1 bg-slate-600 rounded-lg p-1">
                {pages.map((page) => (
                    <button
                        key={page}
                        onClick={() => onPageChange(page)}
                        className={`min-w-[40px] h-10 px-3 rounded-md font-medium transition-all ${
                            currentPage === page
                                ? 'bg-white text-slate-900'
                                : 'text-white hover:bg-slate-500'
                        }`}
                    >
                        {page}
                    </button>
                ))}
            </div>
        </div>
    );
}