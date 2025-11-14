'use client'
import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { getSafeImageUrl } from '@/app/lib/utils';

const BookHeroSection = () => {
    const [activeSlide, setActiveSlide] = useState(0);

    const slides = [
        {
            title: "Explore The Book World",
            description: "We've put together a list of timeless classics everyone should read at least once. These books have shaped cultures and continue to inspire readers with their lasting wisdom and beauty.",
            imageUrl: null, // Будет приходить с бэкенда
        },
        {
            title: "Discover Science Fiction",
            description: "Journey through space and time with these groundbreaking science fiction novels that have redefined the genre and sparked countless imaginations.",
            imageUrl: null, // Будет приходить с бэкенда
        },
        {
            title: "Mystery & Thriller Classics",
            description: "Dive into these gripping mysteries and thrillers that will keep you on the edge of your seat with their intricate plots and unforgettable characters.",
            imageUrl: null, // Будет приходить с бэкенда
        },
        {
            title: "Fantasy Adventures",
            description: "Embark on magical journeys through enchanted worlds filled with heroes, dragons, and epic quests that have captivated millions of readers worldwide.",
            imageUrl: null, // Будет приходить с бэкенда
        },
    ];

    // Auto-advance slides
    useEffect(() => {
        const timer = setInterval(() => {
            setActiveSlide((prev) => (prev + 1) % slides.length);
        }, 5000);
        return () => clearInterval(timer);
    }, [slides.length]);

    const currentSlide = slides[activeSlide];

    return (
        <div className="w-full py-12 px-6">
            <div className="max-w-7xl mx-auto">
                <div className="bg-white rounded-4xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <div className="relative" style={{ minHeight: '600px' }}>
                        {/* Slides container */}
                        {slides.map((slide, index) => (
                            <div
                                key={index}
                                className={`grid grid-cols-1 lg:grid-cols-2 gap-12 items-center transition-opacity duration-500 ${
                                    index === activeSlide
                                        ? 'opacity-100 relative z-10'
                                        : 'opacity-0 absolute inset-0 z-0 pointer-events-none'
                                }`}
                            >
                                {/* Left side - Text content */}
                                <div className="space-y-6">
                                    <h1 className="text-4xl md:text-5xl font-bold text-gray-800 leading-tight">
                                        {slide.title}
                                    </h1>

                                    <p className="text-base md:text-lg text-gray-600 leading-relaxed">
                                        {slide.description}
                                    </p>

                                    <button className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-800 border border-gray-300 px-6 py-3 rounded-lg font-medium transition-all duration-300">
                                        READ MORE
                                        <span className="text-gray-600">→</span>
                                    </button>

                                    {/* Pagination dots - 4 circles */}
                                    <div className="flex items-center gap-3 pt-4">
                                        {slides.map((_, dotIndex) => (
                                            <button
                                                key={dotIndex}
                                                onClick={() => setActiveSlide(dotIndex)}
                                                className={`rounded-full transition-all duration-300 ${
                                                    dotIndex === activeSlide
                                                        ? 'w-4 h-4 border-2 border-gray-700'
                                                        : 'w-3 h-3 border border-gray-400 hover:border-gray-600'
                                                }`}
                                                aria-label={`Go to slide ${dotIndex + 1}`}
                                            />
                                        ))}
                                    </div>
                                </div>

                                {/* Right side - Image/Illustration */}
                                <div className="relative h-96 lg:h-[500px] rounded-xl overflow-hidden bg-gray-100">
                                    <Image
                                        src={getSafeImageUrl(slide.imageUrl)}
                                        alt={slide.title}
                                        fill
                                        className="object-cover transition-opacity duration-500"
                                        unoptimized={true}
                                        sizes="(max-width: 1024px) 100vw, 50vw"
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BookHeroSection;