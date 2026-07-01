const BASE_URL = 'http://localhost:8000';

async function requestAPI(endpoint, method = 'GET', bodyData = null) {

    const accessToken = localStorage.getItem('access_token');

    const cleanEndpoint = endpoint.trim().startsWith('/')
        ? endpoint.trim()
        : '/' + endpoint.trim();

    const finalURL = `${BASE_URL}${cleanEndpoint}`;

    console.log('REQUEST URL:', finalURL);

    const config = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
    }

    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    const response = await fetch(finalURL, config);

    // INTERCEPTOR 401: token invalid/expired -> bersihkan sesi & redirect login
    if (response.status === 401) {
        alert('Sesi Anda telah habis atau Anda belum login.');
        localStorage.clear();
        window.location.hash = '#login';
        return { status: 401, data: null };
    }

    const data = await response.json();

    return {
        status: response.status,
        data: data
    };
}