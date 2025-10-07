const API_URL = 'http://localhost:8000'

const getHeaders = async () => {
	return {
		'Content-Type': 'application/json'
	}
}

export { API_URL, getHeaders }
