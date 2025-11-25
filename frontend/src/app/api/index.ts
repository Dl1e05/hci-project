const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

const getHeaders = async () => {
	return {
		'Content-Type': 'application/json'
	}
}

export { API_URL, getHeaders }
