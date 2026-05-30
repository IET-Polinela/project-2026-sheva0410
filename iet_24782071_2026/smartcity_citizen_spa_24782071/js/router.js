const routes = {

    '#login': `
        <div class="row justify-content-center mt-5">

            <div class="col-12 col-md-5 col-lg-4 spa-card card shadow-lg p-4 rounded-4">

                <div class="text-center mb-4">
                    <i class="bi bi-person-circle fs-1 text-soft"></i>
                    <h3 class="fw-bold mt-2">
                        Login Warga
                    </h3>
                    <p class="text-soft mb-0">
                        Masuk ke Portal Smart City
                    </p>
                </div>

                <form id="loginForm">

                    <input
                        type="text"
                        id="loginUsername"
                        class="form-control mb-3"
                        placeholder="Username"
                        required
                    >

                    <input
                        type="password"
                        id="loginPassword"
                        class="form-control mb-3"
                        placeholder="Password"
                        required
                    >

                    <button
                        type="submit"
                        class="btn btn-purple w-100 fw-semibold"
                    >
                        <i class="bi bi-box-arrow-in-right me-2"></i>
                        Masuk
                    </button>

                </form>

            </div>

        </div>
    `,


    '#dashboard': `
        <section class="hero-card text-center p-5 mb-4 shadow-lg">
            <h1 class="fw-bold display-5">
                Bandar Lampung Smart City Reporting
            </h1>

            <p class="lead text-soft">
                Laporkan permasalahan kota dengan cepat dan mudah
            </p>
        </section>

        <div class="row g-4">

            <aside class="col-12 col-lg-3">

                <div class="spa-card card border-0 shadow-sm rounded-4 p-3 sticky-top" style="top: 20px;">

                    <button class="btn btn-purple w-100 mb-3 fw-semibold">
                        <i class="bi bi-plus-circle-fill me-2"></i>
                        Laporan Baru
                    </button>

                    <div class="small text-soft">
                        Buat laporan baru sebagai draft sebelum dikirim.
                    </div>

                </div>

            </aside>


            <section class="col-12 col-lg-6">

                <div class="spa-card card border-0 p-5 shadow-sm text-center rounded-4">

                    <i class="bi bi-megaphone fs-1 mb-3"></i>

                    <h4 class="fw-bold">
                        Selamat Datang
                    </h4>

                    <p class="text-soft">
                        Portal warga aktif. Data laporan akan ditampilkan pada tahap praktikum berikutnya.
                    </p>

                </div>

            </section>


            <aside class="col-12 col-lg-3">

                <div class="spa-card card border-0 p-3 shadow-sm rounded-4 sticky-top" style="top: 20px;">

                    <div class="fw-bold mb-3">
                        <i class="bi bi-shield-check me-2"></i>
                        Pengumuman
                    </div>

                    <p class="text-soft mb-0">
                        Smart City SPA Active
                    </p>

                </div>

            </aside>

        </div>
    `
};



function handleRouting() {

    const hash = window.location.hash || '#login';

    document.getElementById('app-content').innerHTML =
        routes[hash] || routes['#login'];


    if (hash === '#login') {

        if (typeof setupLoginForm === 'function') {
            setupLoginForm();
        }

    }

}


window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);