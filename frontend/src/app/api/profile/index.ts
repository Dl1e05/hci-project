import { API_URL } from "@/app/api";

export interface UserProfile {
    first_name?: string; // соответствует полям в изображении
    last_name?: string;
    birth_date: string;
    language?: string;
    language_level?: string;
    email: string;
    phone_number?: string;
    username: string;
}

export async function fetchUserProfile(): Promise<UserProfile> {
    try {
        const response = await fetch(`${API_URL}/profile/me`, { // Проверьте ваш URL
            method: 'GET',
            headers: { 'Content-Type': 'application/json'}, // Должно содержать Access Token
            credentials: 'include'
        })

        // Аналогичная обработка ответа, как и в функции register
        const contentType = response.headers.get('content-type') || ''
        const isJson = contentType.includes('application/json')
        const data = isJson ? await response.json() : await response.text()

        if (!response.ok) {
            const detail = isJson ? (data?.detail || data?.message) : undefined
            const message = Array.isArray(detail) ? (detail[0]?.msg || 'Failed to fetch profile') : (detail || 'Failed to fetch profile')
            throw new Error(message)
        }

        return data as UserProfile
    } catch (error) {
        console.error('Fetch profile error:', error)
        throw error
    }
}