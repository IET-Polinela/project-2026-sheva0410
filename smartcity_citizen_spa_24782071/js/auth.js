function setupLoginForm() {

    const form = document.getElementById('loginForm');

    if (!form) {
        console.log('Login form tidak ditemukan');
        return;
    }

    form.addEventListener('submit', async function (event) {

        event.preventDefault();

        const username =
            document.getElementById('loginUsername').value.trim();

        const password =
            document.getElementById('loginPassword').value;

        try {

            const response = await requestAPI(
                '/api/token/',
                'POST',
                {
                    username: username,
                    password: password
                }
            );

            console.log('LOGIN RESPONSE:', response);

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

                if (typeof renderPage === 'function') {
                    renderPage();
                } else if (typeof router === 'function') {
                    router();
                } else {
                    window.location.reload();
                }

            }

            else {

                alert(
                    'Login gagal.\n' +
                    'Status: ' + response.status + '\n' +
                    'Detail: ' + JSON.stringify(response.data)
                );

            }

        } catch (error) {

            console.error('LOGIN ERROR:', error);
            alert('Login error. Cek Console browser.');

        }

    });

}



function setupRegisterForm() {

    const form = document.getElementById('registerForm');

    if (!form) {
        console.log('Register form tidak ditemukan');
        return;
    }

    form.addEventListener('submit', async function (event) {

        event.preventDefault();

        const username =
            document.getElementById('registerUsername').value.trim();

        const email =
            document.getElementById('registerEmail').value.trim();

        const password =
            document.getElementById('registerPassword').value;

        try {

            const response = await requestAPI(
                '/api/auth/register/',
                'POST',
                {
                    username: username,
                    email: email,
                    password: password
                }
            );

            console.log('REGISTER RESPONSE:', response);

            if (response.status === 201) {

                alert('Registrasi berhasil! Silakan login.');

                window.location.hash = '#login';

                if (typeof renderPage === 'function') {
                    renderPage();
                } else if (typeof router === 'function') {
                    router();
                } else {
                    window.location.reload();
                }

            }

            else {

                alert(
                    'Registrasi gagal.\n' +
                    'Status: ' + response.status + '\n' +
                    'Detail: ' + JSON.stringify(response.data)
                );

            }

        } catch (error) {

            console.error('REGISTER ERROR:', error);
            alert('Register error. Cek Console browser.');

        }

    });

}
