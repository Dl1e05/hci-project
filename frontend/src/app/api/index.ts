const API_URL = 'http://localhost:8001'

const getHeaders = async () => {
	return {
		'Content-Type': 'application/json'
	}
}

export { API_URL, getHeaders }
