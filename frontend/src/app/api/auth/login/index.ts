import { API_URL, getHeaders } from "../..";


type LoginPayload = {
  username_or_email: string;
  password: string;
  is_remember_me: boolean;
};

export async function login(payload: LoginPayload) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: await getHeaders(),
        credentials: 'include',
        body: JSON.stringify(payload)   
    })
    const contentType = response.headers.get('content-type') || ''
    const isJson = contentType.includes('application/json')
    const data = isJson ? await response.json() : await response.text()

    if (!response.ok) {
      const message = isJson ? (data?.detail || data?.message || 'Login failed') : (data || 'Login failed')
      new Error(message)
    }

    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

