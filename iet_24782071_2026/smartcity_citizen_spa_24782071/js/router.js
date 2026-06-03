const routes = {

    '#login': `
        <div class="row justify-content-center mt-5">

            <div class="col-12 col-md-5 col-lg-4 spa-card card shadow-lg p-4 rounded-4">

                <div class="text-center mb-4">
                    <i class="bi bi-person-circle fs-1 text-soft"></i>
                    <h3 class="fw-bold mt-2">Login Warga</h3>
                    <p class="text-soft mb-0">Masuk ke Portal Smart City</p>
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

                    <button type="submit" class="btn btn-purple w-100 fw-semibold">
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

                    <button
                        class="btn btn-purple w-100 mb-3 fw-semibold"
                        id="openCreateModalBtn"
                        type="button"
                    >
                        <i class="bi bi-plus-circle-fill me-2"></i>
                        Laporan Baru
                    </button>

                    <div class="small text-soft mb-3">
                        Buat laporan baru sebagai draft sebelum dikirim.
                    </div>

                    <hr class="border-light opacity-25">

                    <div class="fw-bold mb-3">
                        <i class="bi bi-bar-chart-fill me-2"></i>
                        Status Laporan Anda
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-soft">
                            <i class="bi bi-pencil-square me-1"></i>
                            Draft
                        </span>
                        <span class="badge bg-secondary" id="draftCount">0</span>
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-soft">
                            <i class="bi bi-send-fill me-1"></i>
                            Diajukan
                        </span>
                        <span class="badge bg-primary" id="reportedCount">0</span>
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-soft">
                            <i class="bi bi-patch-check-fill me-1"></i>
                            Terverifikasi
                        </span>
                        <span class="badge bg-info text-dark" id="verifiedCount">0</span>
                    </div>

                    <div class="d-flex justify-content-between mb-2">
                        <span class="text-soft">
                            <i class="bi bi-gear-fill me-1"></i>
                            Diproses
                        </span>
                        <span class="badge bg-warning text-dark" id="progressCount">0</span>
                    </div>

                    <div class="d-flex justify-content-between">
                        <span class="text-soft">
                            <i class="bi bi-check-circle-fill me-1"></i>
                            Selesai
                        </span>
                        <span class="badge bg-success" id="resolvedCount">0</span>
                    </div>

                </div>

            </aside>


            <section class="col-12 col-lg-6">

                <div class="spa-card card border-0 shadow-sm rounded-4 p-3 mb-3">

                    <ul class="nav nav-pills gap-2" id="reportTabs">
                        <li class="nav-item">
                            <button
                                class="nav-link active"
                                id="myReportsTab"
                                type="button"
                                data-tab="my_reports"
                            >
                                <i class="bi bi-person-lines-fill me-1"></i>
                                Laporan Saya
                            </button>
                        </li>

                        <li class="nav-item">
                            <button
                                class="nav-link"
                                id="feedTab"
                                type="button"
                                data-tab="feed"
                            >
                                <i class="bi bi-globe2 me-1"></i>
                                Feed Kota
                            </button>
                        </li>
                    </ul>

                </div>

                <div id="reportListContainer"></div>

                <div id="paginationContainer" class="mt-3"></div>

            </section>


            <aside class="col-12 col-lg-3">

                <div class="spa-card card border-0 p-3 shadow-sm rounded-4 sticky-top" style="top: 20px;">

                    <div class="fw-bold mb-3">
                        <i class="bi bi-shield-check me-2"></i>
                        Pengumuman
                    </div>

                    <p class="text-soft mb-0">
                        Smart City SPA Active. Gunakan tab Laporan Saya untuk mengelola draft,
                        dan Feed Kota untuk melihat laporan publik.
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


    if (hash === '#dashboard') {

        if (typeof initDashboard === 'function') {
            initDashboard();
        }

    }

}


window.addEventListener('hashchange', handleRouting);
window.addEventListener('DOMContentLoaded', handleRouting);