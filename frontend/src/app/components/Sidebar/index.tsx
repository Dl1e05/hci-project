// 📁 components/Sidebar.tsx

import React from 'react';
import { IoApps, IoTimeOutline, IoNotificationsOutline, IoSettingsOutline, IoPersonOutline } from 'react-icons/io5';

// Задаем ширину, например, 80px
const SIDEBAR_WIDTH = '80px';

export default function Sidebar() {
  const icons = [
    { icon: IoApps, key: 'dashboard' },
    { icon: IoTimeOutline, key: 'history' },
    { icon: IoNotificationsOutline, key: 'notifications' },
    { icon: IoPersonOutline, key: 'profile' }, // Добавил иконку профиля
    { icon: IoSettingsOutline, key: 'settings' },
  ];

  return (
      <nav
          // 💡 Ключевые стили: фиксированное позиционирование и цвет фона
          className="fixed top-0 left-0 h-full bg-white border-r border-gray-200 flex flex-col items-center py-6"
          style={{ width: SIDEBAR_WIDTH }}
      >
        {/* Логотип/Квадраты вверху */}
        <div className="mb-10 p-2">
          <div className="grid grid-cols-2 gap-1">
            {/* Имитация вашего логотипа из двух квадратов */}
            <div className="w-4 h-4 bg-blue-500 rounded-sm"></div>
            <div className="w-4 h-4 bg-gray-300 rounded-sm"></div>
            <div className="w-4 h-4 bg-gray-300 rounded-sm"></div>
            <div className="w-4 h-4 bg-blue-500 rounded-sm"></div>
          </div>
        </div>

        {/* Список навигационных иконок */}
        <div className="flex flex-col gap-8">
          {icons.map((item) => (
              <div
                  key={item.key}
                  className="p-3 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer text-gray-500 hover:text-blue-600"
                  // Пример активного состояния:
                  // className={item.key === 'dashboard' ? "p-3 rounded-xl bg-blue-100 text-blue-600" : "..."}
              >
                <item.icon size={28} />
              </div>
          ))}
        </div>
      </nav>
  );
}