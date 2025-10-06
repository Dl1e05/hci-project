'use server'

import { API_URL, getHeaders } from "../..";


type LoginPayload = {
  username_or_email: string;
  password: string;
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
    const responce = await fetch(`${API_URL}/auth/login/`, {
        method: 'POST',
        headers: await getHeaders(),
        body: JSON.stringify(payload)   
    })
    const data = await responce.json()
    return data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

