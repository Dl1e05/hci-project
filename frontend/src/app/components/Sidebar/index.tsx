'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    IoApps,
    IoTimeOutline,
    IoNotificationsOutline,
    IoSettingsOutline,
    IoPersonOutline,
    IoHeart
} from 'react-icons/io5';

const SIDEBAR_PX = 80;

// Проверяем, является ли путь страницей из папки (content)
function isContentPage(pathname: string): boolean {
    return pathname.startsWith('/watch') || 
           pathname.startsWith('/read') || 
           pathname.startsWith('/play') || 
           pathname.startsWith('/listen');
}

export default function Sidebar() {
    const pathname = usePathname();

    // не рисуем на страницах (content)
    if (isContentPage(pathname)) return null;

    const items = [
        { href: '/',         Icon: IoApps },
        { href: '/personal',  Icon: IoHeart },
        { href: '/analytics', Icon: IoTimeOutline },
        { href: '/settings', Icon: IoSettingsOutline },
    ];

    return (
        <nav
            className="fixed top-0 left-0 h-full bg-white border-r border-gray-200 flex flex-col items-center z-50"
            style={{ width: `${SIDEBAR_PX}px` }}
        >
            <div className="flex flex-col gap-8 pt-[120px] pb-6">
                {items.map(({ href, Icon }) => {
                    const active = pathname === href;
                    return (
                        <Link
                            key={href}
                            href={href}
                            className={`p-3 rounded-xl transition-colors ${active ? 'bg-blue-100 text-blue-600' : 'text-gray-500 hover:bg-gray-100 hover:text-blue-600'}`}
                            aria-current={active ? 'page' : undefined}
                        >
                            <Icon size={28} />
                        </Link>
                    );
                })}
            </div>
        </nav>
    );
}
