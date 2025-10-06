import { headers } from 'next/headers'

const API_URL = 'http://127.0.0.1:8001'

const getHeaders = async () => {
	return {
		'Content-Type': 'application/json',
		...(await headers())
	}
}

export { API_URL, getHeaders }
