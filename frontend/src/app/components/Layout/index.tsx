'use client';

import React, { useState, ReactNode } from 'react';
import Sidebar from '../Sidebar';
import Header from '../Header';
import Footer from '../Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState<boolean>(true);

  const toggleSidebar = (): void => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar isOpen={sidebarOpen} />
      <Header toggleSidebar={toggleSidebar} />
      
      {/* Main content */}
      <main 
        className={`transition-all duration-300 pt-20 ${sidebarOpen ? 'ml-64' : 'ml-16'}`}
        style={{ minHeight: 'calc(100vh - 200px)' }}
      >
        <div className="p-6">
          {children}
        </div>
      </main>

      <div className={`transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'}`}>
        <Footer />
      </div>
    </div>
  );
};

export default Layout;