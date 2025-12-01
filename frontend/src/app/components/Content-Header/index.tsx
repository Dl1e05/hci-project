'use client';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { isAuthenticated } from '@/app/lib/utils';

export default function ContentHeader() {
  const pathname = usePathname();
  const router = useRouter();

  const handleProfileClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const auth = isAuthenticated();
    router.replace(auth ? '/profile' : '/login');
  };

  const navItems = [
    { name: 'Main', href: '/' },
    { name: 'Analytics', href: '/analytics' },
    { name: 'Personal Content', href: '/personal' },
    { name: 'Settings', href: '/settings' }
  ];

  // Определяем активную вкладку на основе pathname
  const getActiveTab = () => {
    if (pathname === '/home' || pathname === '/') return 'Main';
    if (pathname === '/analytics') return 'Analytics';
    if (pathname === '/personal') return 'Personal Content';
    if (pathname === '/settings') return 'Settings';
    return '';
  };

  const activeTab = getActiveTab();

  return (
    <header className="fixed top-6 left-6 right-6 z-50 backdrop-blur-md bg-gray-800/80 rounded-2xl border border-white/20">
      <div className="w-full px-8 py-4 flex items-center justify-between">
        {/* Left: Logo */}
        <div className="flex items-center">
          <Link href="/" className="flex items-center justify-center w-10 h-10 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 hover:bg-white/20 transition-colors">
            <span className="text-xl font-bold text-white">P</span>
          </Link>
        </div>

        {/* Center: Navigation Links */}
        <nav className="flex items-center gap-8">
          {navItems.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="relative text-sm font-medium text-white hover:text-white/80 transition-colors px-3 py-2"
            >
              {item.name}
              {activeTab === item.name && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-white rounded-full" />
              )}
            </Link>
          ))}
        </nav>

        {/* Right: Search + Notifications + Avatar */}
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative">
            <input
              type="text"
              placeholder="Search"
              className="pl-10 pr-4 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-white/50 w-48 bg-white/10 backdrop-blur-sm text-white placeholder:text-white/70 border border-white/20"
            />
            <svg 
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/70" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>

          {/* Notifications */}
          <button
            className="w-10 h-10 flex items-center justify-center text-white hover:bg-white/10 transition-colors rounded-lg border border-white/20 bg-white/10 backdrop-blur-sm"
            aria-label="Notifications"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>

          {/* Avatar */}
          <button
            onClick={handleProfileClick}
            className="w-10 h-10 bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 grid place-items-center hover:bg-white/20 transition-colors cursor-pointer"
            aria-label="Profile"
          >
            <span className="text-lg" role="img" aria-label="avatar">👻</span>
          </button>
        </div>
      </div>
    </header>
  );
}