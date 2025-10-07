import React from 'react';
import { Bell, Search } from 'lucide-react';


const Header: React.FC = () => {
  return (
    <header className="fixed top-0 right-0 left-0 bg-white border-b border-slate-200 z-30">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left side */}
        <div className="flex items-center gap-4">
          <h1 className="text-lg font-semibold text-slate-800">Welcome, user</h1>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search"
              className="pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
            />
          </div>

          {/* Notifications */}
          <button 
            className="p-2 hover:bg-slate-100 rounded-lg transition-colors relative"
            aria-label="Notifications"
          >
            <Bell size={20} className="text-slate-600" />
            <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>

          {/* User Avatar */}
          <button 
            className="w-10 h-10 bg-yellow-400 rounded-full flex items-center justify-center hover:opacity-80 transition-opacity"
            aria-label="User menu"
          >
            <span className="text-sm font-semibold text-white">U</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;