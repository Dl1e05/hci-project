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

export default function Layout({ children, username }: LayoutProps) {
    const pathname = usePathname();
    const showSidebar = pathname !== '/' && pathname !== '/home';

    return (
        <div className="min-h-screen bg-slate-50">
            {/* Sidebar скрыт на главной */}
            {showSidebar && <Sidebar />}

            <Header username={username} hasSidebar={showSidebar} />

            <main style={showSidebar ? { marginLeft: `${SIDEBAR_PX}px` } : undefined}>
                {children}
            </main>

            <Footer />
        </div>
    );
}
