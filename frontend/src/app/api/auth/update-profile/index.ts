// app/api/auth/profile.ts или index.ts (там, где находятся fetchUserProfile и register)

import { API_URL, getHeaders } from "../..";

// Интерфейс для данных, которые могут быть отправлены на обновление
export interface ProfileUpdatePayload {
    first_name?: string;
    last_name?: string;
    birth_date?: string;
    language?: string;
    language_level?: string;
    phone_number?: string;
    // username и email обычно не обновляются через этот эндпоинт
}

export async function updateProfile(payload: ProfileUpdatePayload) {
    try {
        const response = await fetch(`${API_URL}/profile/me`, { // Используйте тот же эндпоинт, что и для GET, но с методом PUT/PATCH
            method: 'PATCH', // ⬅️ Используем PUT или PATCH (зависит от бэкенда). PATCH лучше для частичного обновления.

            // ВАЖНО: Поскольку токены хранятся в HttpOnly cookies,
            // нам нужно убедиться, что они будут отправлены.
            credentials: 'include',

            headers: await getHeaders(), // Должны включать 'Content-Type': 'application/json'
            body: JSON.stringify(payload)
        })

        const contentType = response.headers.get('content-type') || ''
        const isJson = contentType.includes('application/json')
        const data = isJson ? await response.json() : await response.text()

        if (!response.ok) {
            // Обработка ошибок (например, неверные данные)
            const detail = isJson ? (data?.detail || data?.message) : undefined
            const message = Array.isArray(detail) ? (detail[0]?.msg || 'Failed to update profile') : (detail || 'Failed to update profile')
            throw new Error(message)
        }

        // Бэкенд должен вернуть обновленные данные профиля
        return data
    } catch (error) {
        console.error('Update profile error:', error)
        throw error
    }
}