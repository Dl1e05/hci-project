import { API_URL, getHeaders } from "../..";


type RegisterPayload = {
  username: string;
  email: string;
  birth_date: string;
  password: string;
  password_repeat: string;
};

// type RegisterResponce = {
//     message?: string
//     user?: {
//         id: string
//         email?:string--
//         username: string
//     }
//     errors?: Record<string, string[]>
// }

export async function register(payload: RegisterPayload) {
  try {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: await getHeaders(),
        body: JSON.stringify(payload)
    })
    const contentType = response.headers.get('content-type') || ''
    const isJson = contentType.includes('application/json')
    const data = isJson ? await response.json() : await response.text()

    if (!response.ok) {
      // FastAPI often returns {detail: string|array} or field errors
      const detail = isJson ? (data?.detail || data?.message) : undefined
      const message = Array.isArray(detail) ? (detail[0]?.msg || 'Registration failed') : (detail || 'Registration failed')
      throw new Error(message)
    }

    return data
  } catch (error) {
    console.error('Register error:', error)
    throw error
  }
}

