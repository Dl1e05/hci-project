'use server'

import { API_URL, getHeaders } from "../..";


type RegisterPayload = {
  username: string;
  password: string;
  confirmPassword: string;
  email: string;
};

// type RegisterResponce = {
//     message?: string
//     user?: {
//         id: string
//         email?:string
//         username: string
//     }
//     errors?: Record<string, string[]>
// }

export async function register(payload: RegisterPayload) {
  try {
    const responce = await fetch(`${API_URL}`, {
        method: 'POST',
        headers: await getHeaders(),
        body: JSON.stringify(payload)
    })
    const data = await responce.json()
    return data
  } catch (error) {
    console.error('Register error:', error)
    throw error
  }
}

