const BASE_URL = 'http://103.151.63.87:8005';

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

    const data = await response.json();

    return {
        status: response.status,
        data: data
    };
}
