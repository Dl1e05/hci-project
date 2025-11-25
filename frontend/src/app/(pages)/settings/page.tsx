'use client';

import React, { useState } from 'react';
import Layout from '@/app/components/Layout';
import Input from '@/app/components/Input';

interface ToggleProps {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}

function Toggle({ label, checked, onChange }: ToggleProps) {
  return (
    <div className="flex items-center justify-between mb-8">
      <span className="text-gray-700 text-base font-medium">{label}</span>
      <button
        type="button"
        onClick={() => onChange(!checked)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          checked ? 'bg-green-500' : 'bg-gray-300'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            checked ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  );
}

interface DropdownProps {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}

function Dropdown({ label, value, options, onChange }: DropdownProps) {
  return (
    <div className="mb-8">
      <label className="block text-gray-700 text-base font-medium mb-3">{label}</label>
      <div className="relative">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="w-full h-14 text-base px-4 rounded-xl bg-gray-100 border border-gray-100 text-gray-800 appearance-none cursor-pointer focus:outline-none focus:bg-white focus:border-gray-300 focus:ring-2 focus:ring-gray-200 pr-10"
        >
          {options.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
        <svg 
          className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
  );
}

export default function SettingsPage() {
  const [streakUpdates, setStreakUpdates] = useState(true);
  const [dailyReminders, setDailyReminders] = useState(true);
  const [news, setNews] = useState(true);
  const [dailyGoal, setDailyGoal] = useState('');
  const [theme, setTheme] = useState('Light');
  const [interfaceLanguage, setInterfaceLanguage] = useState('English');

  const themeOptions = ['Light', 'Dark', 'Auto'];
  const languageOptions = ['English', 'Russian', 'Ukrainian', 'Spanish', 'French'];

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        <div className="min-h-[60vh] flex items-center justify-center">
          <div className="bg-white rounded-3xl shadow-lg w-full max-w-6xl 2xl:max-w-7xl overflow-visible">
            <div className="px-12 md:px-16 lg:px-20 py-12 md:py-16">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8">
                {/* Left Column */}
                <div>
                  {/* Notifications Section */}
                  <div className="mb-10">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-6">Notifications</h2>
                    <Toggle
                      label="Streak updates"
                      checked={streakUpdates}
                      onChange={setStreakUpdates}
                    />
                    <Toggle
                      label="Daily reminders"
                      checked={dailyReminders}
                      onChange={setDailyReminders}
                    />
                    <Toggle
                      label="News"
                      checked={news}
                      onChange={setNews}
                    />
                  </div>

                  {/* Daily Goal Section */}
                  <div>
                    <h2 className="text-2xl font-semibold text-gray-800 mb-6">Daily Goal</h2>
                    <Input
                      type="text"
                      value={dailyGoal}
                      onChange={(e) => setDailyGoal(e.target.value)}
                      placeholder="Enter your daily goal"
                      size="md"
                      className="bg-gray-100"
                    />
                  </div>
                </div>

                {/* Right Column */}
                <div>
                  <h2 className="text-2xl font-semibold text-gray-800 mb-6">Other settings</h2>
                  <Dropdown
                    label="Theme"
                    value={theme}
                    options={themeOptions}
                    onChange={setTheme}
                  />
                  <Dropdown
                    label="Interface language"
                    value={interfaceLanguage}
                    options={languageOptions}
                    onChange={setInterfaceLanguage}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
