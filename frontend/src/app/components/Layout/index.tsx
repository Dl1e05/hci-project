'use client';

import React, { useState, ReactNode } from 'react';
import Sidebar from '../Sidebar';
import Header from '../Header';
import Footer from '../Footer';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <Header  />

      {/* Main content */}
      <main>
        <div className="p-6">
          {children}
        </div>
      </main>


        <Footer />
    </div>
  );
};

export default Layout;