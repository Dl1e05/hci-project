'use client';

import React, { useLayoutEffect } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/app/components/Layout';
import { isAuthenticated } from '@/app/lib/utils';

export default function SettingsPage() {
  const router = useRouter();
  
  // Моментальная проверка авторизации - выполняется синхронно до рендера
  useLayoutEffect(() => {
    if (!isAuthenticated()) {
      router.replace('/login');
    }
  }, [router]);

  // Если не авторизован, не рендерим ничего (редирект уже в процессе)
  if (!isAuthenticated()) {
    return null;
  }

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        <div className="bg-white rounded-xl shadow p-6 text-gray-600">
          Settings page content will be here.
        </div>
      </div>
    </Layout>
  );
}
