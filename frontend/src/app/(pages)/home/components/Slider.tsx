'use client'
import React, { useState, useEffect } from 'react';

const BookHeroSection = () => {
    const [activeSlide, setActiveSlide] = useState(0);

    const slides = [
        {
            title: "Explore The Book World",
            description: "We've put together a list of timeless classics everyone should read at least once. These books have shaped cultures and continue to inspire readers with their lasting wisdom and beauty.",
            books: [
                { title: "The Great Gatsby", color: "bg-blue-900", rotate: "-rotate-6", top: "top-0", left: "left-8" },
                { title: "To Kill a Mockingbird", color: "bg-gray-800", rotate: "rotate-3", top: "top-16", left: "left-4" },
                { title: "BELOVED", color: "bg-red-700", rotate: "rotate-6", top: "top-0", left: "left-40" },
                { title: "Toni Morrison", color: "bg-gray-600", rotate: "-rotate-3", top: "top-12", left: "left-56" },
                { title: "GONE WITH THE WIND", color: "bg-yellow-500", rotate: "rotate-12", top: "top-28", left: "left-44", large: true },
                { title: "ONE FLEW OVER", color: "bg-orange-700", rotate: "-rotate-12", top: "top-4", right: "right-8" },
                { title: "THE JUNGLE", color: "bg-green-800", rotate: "rotate-6", top: "top-40", left: "left-20" },
                { title: "OF MICE AND MEN", color: "bg-amber-700", rotate: "-rotate-6", top: "top-52", left: "left-60" },
                { title: "Catcher in the Rye", color: "bg-red-600", rotate: "rotate-3", top: "top-20", right: "right-0" },
                { title: "The Color Purple", color: "bg-purple-300", rotate: "-rotate-6", top: "top-56", right: "right-4", light: true },
            ]
        },
        {
            title: "Discover Science Fiction",
            description: "Journey through space and time with these groundbreaking science fiction novels that have redefined the genre and sparked countless imaginations.",
            books: [
                { title: "Dune", color: "bg-orange-800", rotate: "rotate-6", top: "top-4", left: "left-12" },
                { title: "1984", color: "bg-gray-900", rotate: "-rotate-3", top: "top-24", left: "left-8" },
                { title: "Foundation", color: "bg-blue-700", rotate: "rotate-12", top: "top-8", left: "left-44" },
                { title: "Neuromancer", color: "bg-cyan-600", rotate: "-rotate-6", top: "top-16", left: "left-64" },
                { title: "Brave New World", color: "bg-teal-700", rotate: "rotate-3", top: "top-36", left: "left-36", large: true },
                { title: "Fahrenheit 451", color: "bg-red-800", rotate: "-rotate-12", top: "top-0", right: "right-12" },
                { title: "Ender's Game", color: "bg-indigo-700", rotate: "rotate-6", top: "top-44", left: "left-16" },
                { title: "Hyperion", color: "bg-purple-800", rotate: "-rotate-3", top: "top-60", left: "left-52" },
                { title: "Snow Crash", color: "bg-slate-700", rotate: "rotate-9", top: "top-24", right: "right-4" },
                { title: "The Martian", color: "bg-orange-600", rotate: "-rotate-6", top: "top-52", right: "right-8" },
            ]
        },
        {
            title: "Mystery & Thriller Classics",
            description: "Dive into these gripping mysteries and thrillers that will keep you on the edge of your seat with their intricate plots and unforgettable characters.",
            books: [
                { title: "Sherlock Holmes", color: "bg-amber-900", rotate: "-rotate-6", top: "top-2", left: "left-10" },
                { title: "The Girl with the Dragon Tattoo", color: "bg-black", rotate: "rotate-6", top: "top-20", left: "left-6" },
                { title: "Gone Girl", color: "bg-pink-700", rotate: "rotate-3", top: "top-6", left: "left-42" },
                { title: "The Da Vinci Code", color: "bg-red-900", rotate: "-rotate-12", top: "top-14", left: "left-58" },
                { title: "Murder on the Orient Express", color: "bg-blue-800", rotate: "rotate-9", top: "top-32", left: "left-40", large: true },
                { title: "The Silent Patient", color: "bg-teal-900", rotate: "-rotate-6", top: "top-4", right: "right-10" },
                { title: "In Cold Blood", color: "bg-gray-700", rotate: "rotate-6", top: "top-42", left: "left-18" },
                { title: "Big Little Lies", color: "bg-cyan-800", rotate: "-rotate-3", top: "top-56", left: "left-54" },
                { title: "The Maltese Falcon", color: "bg-yellow-700", rotate: "rotate-12", top: "top-22", right: "right-2" },
                { title: "Rebecca", color: "bg-rose-800", rotate: "-rotate-9", top: "top-54", right: "right-6" },
            ]
        },
        {
            title: "Fantasy Adventures",
            description: "Embark on magical journeys through enchanted worlds filled with heroes, dragons, and epic quests that have captivated millions of readers worldwide.",
            books: [
                { title: "The Lord of the Rings", color: "bg-green-900", rotate: "rotate-3", top: "top-0", left: "left-8" },
                { title: "Harry Potter", color: "bg-red-800", rotate: "-rotate-6", top: "top-18", left: "left-4" },
                { title: "A Song of Ice and Fire", color: "bg-gray-800", rotate: "rotate-9", top: "top-4", left: "left-40" },
                { title: "The Hobbit", color: "bg-amber-800", rotate: "-rotate-3", top: "top-16", left: "left-60" },
                { title: "The Name of the Wind", color: "bg-orange-700", rotate: "rotate-6", top: "top-30", left: "left-44", large: true },
                { title: "Mistborn", color: "bg-slate-800", rotate: "-rotate-12", top: "top-2", right: "right-8" },
                { title: "The Way of Kings", color: "bg-blue-900", rotate: "rotate-6", top: "top-40", left: "left-20" },
                { title: "The Wheel of Time", color: "bg-purple-900", rotate: "-rotate-6", top: "top-54", left: "left-58" },
                { title: "Eragon", color: "bg-cyan-700", rotate: "rotate-12", top: "top-20", right: "right-0" },
                { title: "The Chronicles of Narnia", color: "bg-yellow-600", rotate: "-rotate-3", top: "top-56", right: "right-4" },
            ]
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
        <div className="min-h-screen bg-gradient-to-br from-slate-200 to-slate-300 flex items-center justify-center p-6">
            <div className="max-w-7xl w-full bg-white rounded-3xl shadow-2xl p-8 md:p-12 relative overflow-hidden">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                    {/* Left side - Text content */}
                    <div className="space-y-6">
                        <h1 className="text-4xl md:text-5xl font-bold text-slate-700 leading-tight transition-all duration-500">
                            {currentSlide.title}
                        </h1>

                        <p className="text-base md:text-lg text-slate-500 leading-relaxed transition-all duration-500">
                            {currentSlide.description}
                        </p>

                        <button className="flex items-center gap-3 bg-slate-600 hover:bg-slate-700 text-white px-6 md:px-8 py-3 md:py-4 rounded-full font-medium transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-105">
                            READ MORE
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </button>

                        {/* Pagination dots */}
                        <div className="flex items-center gap-3 pt-8">
                            {slides.map((_, index) => (
                                <button
                                    key={index}
                                    onClick={() => setActiveSlide(index)}
                                    className={`rounded-full transition-all duration-300 ${
                                        index === activeSlide
                                            ? 'w-12 h-3 bg-slate-600'
                                            : 'w-3 h-3 bg-slate-300 hover:bg-slate-400'
                                    }`}
                                    aria-label={`Go to slide ${index + 1}`}
                                />
                            ))}
                        </div>
                    </div>

                    {/* Right side - Books display */}
                    <div className="relative h-96 lg:h-[500px]">
                        {currentSlide.books.map((book, index) => (
                            <div
                                key={index}
                                className={`absolute ${book.top} ${book.left || ''} ${book.right || ''} ${
                                    book.large ? 'w-28 h-40' : 'w-24 h-36'
                                } ${book.color} rounded shadow-xl transform ${book.rotate} 
                flex items-center justify-center transition-all duration-700 ease-in-out
                hover:scale-110 hover:z-50 hover:shadow-2xl cursor-pointer
                animate-[fadeIn_0.5s_ease-in-out]`}
                                style={{
                                    animationDelay: `${index * 0.1}s`,
                                    animationFillMode: 'backwards'
                                }}
                            >
                                <div className={`${book.light ? 'text-purple-900' : 'text-white'} text-xs font-bold text-center px-2`}>
                                    {book.title}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.9);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
      `}</style>
        </div>
    );
};

export default BookHeroSection;