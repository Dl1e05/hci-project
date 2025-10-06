'use server'

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
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Register error:', error)
    throw error
  }
}

