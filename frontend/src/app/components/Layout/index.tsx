'use client';
import React from 'react';
import { usePathname } from 'next/navigation';
import Sidebar from '../Sidebar';
import Header from '../Header';
import Footer from '../Footer';

interface LayoutProps {
    children: React.ReactNode;
    username?: string;
}

const SIDEBAR_PX = 80;

// Проверяем, является ли путь страницей из папки (content)
function isContentPage(pathname: string): boolean {
    return pathname.startsWith('/watch') || 
           pathname.startsWith('/read') || 
           pathname.startsWith('/play') || 
           pathname.startsWith('/listen');
}

export default function Layout({ children, username }: LayoutProps) {
    const pathname = usePathname();
    const showSidebar = !isContentPage(pathname);

    return (
        <div className="min-h-dvh flex flex-col" style={{ backgroundColor: '#F9F9F9' }}>
            {showSidebar && <Sidebar />}

            {/* одна колонка справа от сайдбара */}
            <div style={showSidebar ? { marginLeft: `${SIDEBAR_PX}px` } : undefined} className="flex flex-col min-h-dvh">
                <Header username={username} hasSidebar={showSidebar} />
                <main className="flex-1">{children}</main>
                <Footer />
            </div>
        </div>
    );
}
