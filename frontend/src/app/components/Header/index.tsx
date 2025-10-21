'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface HeaderProps {
  username?: string;
  hasSidebar?: boolean;
}

const SIDEBAR_PX = 80;

const NAV = [
  { href: '/home',               label: 'Main' },
  { href: '/analytics',      label: 'Analytics' },
  { href: '/personal-content', label: 'Personal Content' },
  { href: '/settings',       label: 'Settings' },
];

export default function Header({ username, hasSidebar }: HeaderProps) {
  const pathname = usePathname();
  const onMain = pathname === '/home';

  return (
      <header
          className={`py-4 px-6 ${onMain ? 'bg-white border-b border-gray-200' : 'bg-gray-100'}`}
          style={hasSidebar ? { marginLeft: `${SIDEBAR_PX}px` } : undefined}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* left */}
          <div className="flex items-center gap-8">
            {onMain ? (
                <>
                  <Link href="/" className="flex items-center gap-2">
                    <div className="w-10 h-10 bg-slate-700 rounded-lg grid place-items-center">
                      <span className="text-white font-bold">TC</span>
                    </div>
                    <span className="font-semibold text-lg">TheCompany</span>
                  </Link>

                  <nav className="hidden md:flex items-center gap-6">
                    {NAV.map(({ href, label }) => {
                      const active = pathname === href;
                      return (
                          <Link
                              key={href}
                              href={href}
                              className={active ? 'text-slate-700 font-medium' : 'text-gray-500 hover:text-slate-700'}
                              aria-current={active ? 'page' : undefined}
                          >
                            {label}
                          </Link>
                      );
                    })}
                  </nav>
                </>
            ) : (
                <h1 className="text-xl font-medium text-gray-700">Welcome, {username || 'user'}</h1>
            )}
          </div>

          {/* right */}
          <div className="flex items-center gap-4">
            <div className="relative">
              <input
                  type="text"
                  placeholder="Search"
                  className={`pl-10 pr-4 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-500 w-64 ${
                      onMain ? 'bg-gray-100' : 'bg-white'
                  }`}
              />
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <button className={`p-2 rounded-lg transition-colors ${onMain ? 'hover:bg-gray-100' : 'hover:bg-gray-200'}`} aria-label="Notifications">
              <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>

            <Link href="/profile" className="w-10 h-10 bg-yellow-400 rounded-full grid place-items-center hover:opacity-80 transition-opacity">
              <span className="text-lg" role="img" aria-label="avatar">😊</span>
            </Link>
          </div>
        </div>
      </header>
  );
}
