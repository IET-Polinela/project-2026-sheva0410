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