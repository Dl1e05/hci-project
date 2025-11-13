'use client';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { isAuthenticated } from '@/app/lib/utils';

interface HeaderProps {
  username?: string;
  hasSidebar?: boolean;
}

const SIDEBAR_PX = 80;

function getTitle(pathname: string): { text: string; href?: string } {
  if (!pathname || pathname === '/') return { text: 'Welcome' };
  const map: Record<string, { text: string; href?: string }> = {
    '/home': { text: 'Home' },
    '/catalog': { text: 'Catalog' },
    '/play': { text: 'Play' },
    '/personal': { text: 'Personal', href: '/personal' },
    '/profile': { text: 'Profile', href: '/profile' },
    '/analytics': { text: 'Your Analytics' },
    '/settings': { text: 'Settings' },
  };
  // Exact match first
  if (map[pathname]) return map[pathname];
  // Match by first segment for nested routes like /catalog/..., /watch/[id]
  const first = '/' + pathname.split('/').filter(Boolean)[0];
  if (map[first]) return map[first];
  // Fallback: prettify last segment
  const last = pathname.split('/').filter(Boolean).pop() || '';
  const pretty = last.replace(/[-_]/g, ' ')
    .replace(/\b\w/g, (m) => m.toUpperCase());
  return { text: pretty || 'App' };
}

export default function Header({ username, hasSidebar }: HeaderProps) {
  const pathname = usePathname();
  const router = useRouter();
  const t = getTitle(pathname);

  const handleProfileClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    // Сразу проверяем авторизацию синхронно
    const auth = isAuthenticated();
    // Используем replace, чтобы не добавлять в историю и сразу редиректить
    router.replace(auth ? '/profile' : '/login');
  };

  return (
      <header
          className="py-5 px-6 bg-[#F9F9F9]"
          style={hasSidebar ? { marginLeft: `${SIDEBAR_PX}px` } : undefined}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Left: dynamic page title */}
          <div className="min-w-0">
            {t.href ? (
              <Link href={t.href} className="text-3xl font-semibold text-slate-800 hover:text-slate-900 truncate">
                {t.text}
              </Link>
            ) : (
              <span className="text-3xl font-semibold text-slate-800 truncate">{t.text}</span>
            )}
          </div>

          {/* Right: search + avatar */}
          <div className="flex items-center gap-4">
            <div className="relative">
              <input
                  type="text"
                  placeholder="Search"
                  className="pl-10 pr-4 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-slate-500 w-64 bg-gray-100"
              />
              <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <button
              onClick={handleProfileClick}
              className="w-10 h-10 bg-yellow-400 rounded-full grid place-items-center hover:opacity-80 transition-opacity cursor-pointer"
              aria-label="Profile"
            >
              <span className="text-lg" role="img" aria-label="avatar">😊</span>
            </button>
          </div>
        </div>
      </header>
  );
}
