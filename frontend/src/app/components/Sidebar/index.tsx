import React from 'react';
import { Home, Settings, Users, FileText, LucideIcon } from 'lucide-react';

interface MenuItem {
  icon: LucideIcon;
  label: string;
  active?: boolean;
  href?: string;
}

interface SidebarProps {
  isOpen: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  const menuItems: MenuItem[] = [
    { icon: Home, label: 'Dashboard', active: true, href: '/' },
    { icon: Users, label: 'Users', href: '/users' },
    { icon: FileText, label: 'Documents', href: '/documents' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ];

  return (
    <aside className={`fixed left-0 top-0 h-full bg-slate-100 transition-all duration-300 z-40 ${isOpen ? 'w-64' : 'w-16'}`}>
      <div className="flex flex-col h-full">
        {/* Sidebar Header */}
        <div className="p-4 border-b border-slate-300">
          <div className="flex items-center justify-center">
            <div className="w-8 h-8 bg-blue-600 rounded-lg"></div>
          </div>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item, index) => (
            <button
              key={index}
              className={`w-full flex items-center gap-3 px-3 py-3 rounded-lg transition-colors ${
                item.active 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-600 hover:bg-slate-200'
              }`}
              title={item.label}
            >
              <item.icon size={20} />
              {isOpen && <span className="text-sm font-medium">{item.label}</span>}
            </button>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default Sidebar;