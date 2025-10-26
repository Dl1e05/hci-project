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
      let message = 'Login failed'
      
      if (isJson) {
        // Handle validation errors (422)
        if (response.status === 422 && data?.detail) {
          if (Array.isArray(data.detail)) {
            // Multiple validation errors
            message = data.detail.map((err: any) => err.msg || err.message).join(', ')
          } else {
            message = data.detail
          }
        } else {
          // Other errors
          message = data?.detail || data?.message || 'Login failed'
        }
      } else {
        message = data || 'Login failed'
      }
      
      throw new Error(message)
    }

    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

