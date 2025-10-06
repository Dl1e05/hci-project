'use server'

import { API_URL, getHeaders } from "../..";


type LoginPayload = {
  username_or_email: string;
  password: string;
  is_remember_me: boolean;
};

// type LoginResponce = {
//     access_token?: string
//     refresh_token?: string
//     user?: {
//         id: number
//         email: string
//         username: string
//     }
//     message?: string
// }

export async function login(payload: LoginPayload) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: await getHeaders(),
        body: JSON.stringify(payload)   
    })
    const data = await response.json()
    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

