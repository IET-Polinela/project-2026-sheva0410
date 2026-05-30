const BASE_URL = 'http://127.0.0.1:8000';


async function requestAPI(endpoint, method = 'GET', bodyData = null) {

    const accessToken = localStorage.getItem('access_token');

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


    const response = await fetch(
        `${BASE_URL}${endpoint}`,
        config
    );


    const data = await response.json();

    return {
        status: response.status,
        data: data
    };
}