function setupLoginForm() {

    const form = document.getElementById('loginForm');

    form.addEventListener('submit', async function (event) {

        event.preventDefault();

        const username =
            document.getElementById('loginUsername').value;

        const password =
            document.getElementById('loginPassword').value;

        const response = await requestAPI(
            '/api/token/',
            'POST',
            {
                username: username,
                password: password
            }
        );

        if (response.status === 200) {

            localStorage.setItem(
                'access_token',
                response.data.access
            );

            localStorage.setItem(
                'refresh_token',
                response.data.refresh
            );

            alert('Login berhasil!');

            window.location.hash = '#dashboard';

        }

        else {

            alert('Username atau password salah!');

        }

    });

}



function setupRegisterForm() {

    const form = document.getElementById('registerForm');

    form.addEventListener('submit', async function (event) {

        event.preventDefault();

        const username =
            document.getElementById('registerUsername').value;

        const email =
            document.getElementById('registerEmail').value;

        const password =
            document.getElementById('registerPassword').value;

        const response = await requestAPI(
            '/api/auth/register/',
            'POST',
            {
                username: username,
                email: email,
                password: password
            }
        );

        if (response.status === 201) {

            alert('Registrasi berhasil! Silakan login.');

            window.location.hash = '#login';

        }

        else {

            alert('Registrasi gagal. Username mungkin sudah digunakan.');

        }

    });

}