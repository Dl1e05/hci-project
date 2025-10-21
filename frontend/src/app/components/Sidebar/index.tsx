'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { IoApps, IoTimeOutline, IoNotificationsOutline, IoSettingsOutline, IoPersonOutline } from 'react-icons/io5';

const SIDEBAR_PX = 80;

export default function Sidebar() {
    const pathname = usePathname();

    // не рисуем на главной
    if (pathname === '/') return null;
    if (pathname === '/home') return null;

    const items = [
        { href: '/home',          Icon: IoApps },
        { href: '/history',       Icon: IoTimeOutline },
        { href: '/notifications', Icon: IoNotificationsOutline },
        { href: '/profile',       Icon: IoPersonOutline },
        { href: '/settings',      Icon: IoSettingsOutline },
    ];

    return (
        <nav
            className="fixed top-0 left-0 h-full bg-white border-r border-gray-200 flex flex-col items-center py-6 z-50"
            style={{ width: `${SIDEBAR_PX}px` }}
        >
            <Link href="/home" className="mb-10 p-2">
                <div className="grid grid-cols-2 gap-1">
                    <div className="w-4 h-4 bg-blue-500 rounded-sm" />
                    <div className="w-4 h-4 bg-gray-300 rounded-sm" />
                    <div className="w-4 h-4 bg-gray-300 rounded-sm" />
                    <div className="w-4 h-4 bg-blue-500 rounded-sm" />
                </div>
            </Link>

            <div className="flex flex-col gap-8">
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
