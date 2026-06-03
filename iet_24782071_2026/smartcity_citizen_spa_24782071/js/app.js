let currentTab = 'my_reports';
let currentPage = 1;
let editingReportId = null;


function getStatusLabel(status) {
    const labels = {
        'DRAFT': 'Draft',
        'REPORTED': 'Diajukan',
        'VERIFIED': 'Terverifikasi',
        'IN_PROGRESS': 'Diproses',
        'RESOLVED': 'Selesai'
    };

    return labels[status] || status;
}


function getProgress(status) {
    const progress = {
        'DRAFT': 20,
        'REPORTED': 40,
        'VERIFIED': 60,
        'IN_PROGRESS': 80,
        'RESOLVED': 100
    };

    return progress[status] || 0;
}


function getProgressClass(status) {
    if (status === 'RESOLVED') return 'bg-success';
    if (status === 'IN_PROGRESS') return 'bg-warning';
    if (status === 'VERIFIED') return 'bg-info';
    if (status === 'REPORTED') return 'bg-primary';
    return 'bg-secondary';
}


async function loadDashboardData(tab = currentTab, page = 1) {
    currentTab = tab;
    currentPage = page;

    const response = await requestAPI(
        `/api/report/?tab=${tab}&page=${page}`,
        'GET'
    );

    if (response.status === 200) {
        const paginatedData = response.data;

        renderList(paginatedData.results);
        renderPagination(paginatedData);
        loadSummaryStats();
    } else {
        alert('Gagal mengambil data laporan.');
    }
}


function renderList(reports) {
    const container = document.getElementById('reportListContainer');

    if (!reports || reports.length === 0) {
        container.innerHTML = `
            <div class="spa-card card border-0 rounded-4 p-5 text-center">
                <i class="bi bi-inbox fs-1 mb-3"></i>
                <h5 class="fw-bold">Belum Ada Laporan</h5>
                <p class="text-soft mb-0">Data laporan akan muncul di sini.</p>
            </div>
        `;
        return;
    }

    container.innerHTML = reports.map(report => {
        const progress = getProgress(report.status);
        const progressClass = getProgressClass(report.status);

        const actionButtons = report.status === 'DRAFT' && report.is_owner
            ? `
                <div class="d-flex gap-2 mt-3">
                    <button
                        class="btn btn-sm btn-outline-light"
                        onclick="editDraft(${report.id})"
                        type="button"
                    >
                        <i class="bi bi-pencil-square me-1"></i>
                        Edit
                    </button>

                    <button
                        class="btn btn-sm btn-purple"
                        onclick="submitDraft(${report.id})"
                        type="button"
                    >
                        <i class="bi bi-send-fill me-1"></i>
                        Ajukan
                    </button>
                </div>
            `
            : '';

        return `
            <div class="spa-card card border-0 rounded-4 p-4 mb-3 shadow-sm">

                <div class="d-flex justify-content-between align-items-start gap-3">

                    <div>
                        <h5 class="fw-bold mb-1">
                            ${report.title}
                        </h5>

                        <div class="text-soft small mb-2">
                            <i class="bi bi-geo-alt me-1"></i>
                            ${report.location}
                        </div>
                    </div>

                    <span class="badge bg-dark border">
                        ${getStatusLabel(report.status)}
                    </span>

                </div>

                <p class="text-soft mb-3">
                    ${report.description}
                </p>

                <div class="small mb-2">
                    <i class="bi bi-tag me-1"></i>
                    ${report.category}

                    <span class="ms-2">
                        <i class="bi bi-person-circle me-1"></i>
                        ${report.reporter}
                    </span>
                </div>

                <div class="progress" style="height: 8px;">
                    <div
                        class="progress-bar ${progressClass}"
                        style="width: ${progress}%"
                    ></div>
                </div>

                ${actionButtons}

            </div>
        `;
    }).join('');
}


function renderPagination(data) {
    const container = document.getElementById('paginationContainer');

    const previousDisabled = data.previous ? '' : 'disabled';
    const nextDisabled = data.next ? '' : 'disabled';

    container.innerHTML = `
        <div class="d-flex justify-content-center gap-2">

            <button
                class="btn btn-outline-light btn-sm"
                ${previousDisabled}
                onclick="loadDashboardData(currentTab, currentPage - 1)"
                type="button"
            >
                Previous
            </button>

            <span class="btn btn-purple btn-sm disabled">
                Page ${currentPage}
            </span>

            <button
                class="btn btn-outline-light btn-sm"
                ${nextDisabled}
                onclick="loadDashboardData(currentTab, currentPage + 1)"
                type="button"
            >
                Next
            </button>

        </div>
    `;
}


async function loadSummaryStats() {
    const response = await requestAPI(
        '/api/report/?tab=my_reports&page_size=1000',
        'GET'
    );

    if (response.status !== 200) {
        return;
    }

    const reports = response.data.results;

    document.getElementById('draftCount').innerText =
        reports.filter(report => report.status === 'DRAFT').length;

    document.getElementById('reportedCount').innerText =
        reports.filter(report => report.status === 'REPORTED').length;

    document.getElementById('verifiedCount').innerText =
        reports.filter(report => report.status === 'VERIFIED').length;

    document.getElementById('progressCount').innerText =
        reports.filter(report => report.status === 'IN_PROGRESS').length;

    document.getElementById('resolvedCount').innerText =
        reports.filter(report => report.status === 'RESOLVED').length;
}


function openCreateModal() {
    editingReportId = null;

    document.getElementById('reportModalLabel').innerHTML = `
        <i class="bi bi-pencil-square me-2"></i>
        Buat Laporan Baru
    `;

    document.getElementById('reportForm').reset();

    const modal = new bootstrap.Modal(
        document.getElementById('reportModal')
    );

    modal.show();
}


async function editDraft(id) {
    const response = await requestAPI(
        `/api/report/${id}/`,
        'GET'
    );

    if (response.status !== 200) {
        alert('Gagal mengambil data draft.');
        return;
    }

    const report = response.data;

    editingReportId = id;

    document.getElementById('reportModalLabel').innerHTML = `
        <i class="bi bi-pencil-square me-2"></i>
        Edit Draft Laporan
    `;

    document.getElementById('reportTitle').value = report.title;
    document.getElementById('reportCategory').value = report.category;
    document.getElementById('reportDescription').value = report.description;
    document.getElementById('reportLocation').value = report.location;

    const modal = new bootstrap.Modal(
        document.getElementById('reportModal')
    );

    modal.show();
}


function getReportFormData() {
    return {
        title: document.getElementById('reportTitle').value,
        category: document.getElementById('reportCategory').value,
        description: document.getElementById('reportDescription').value,
        location: document.getElementById('reportLocation').value,
    };
}


async function saveDraft() {
    const bodyData = getReportFormData();

    const endpoint = editingReportId
        ? `/api/report/${editingReportId}/`
        : '/api/report/';

    const method = editingReportId ? 'PUT' : 'POST';

    const response = await requestAPI(
        endpoint,
        method,
        {
            ...bodyData,
            status: 'DRAFT'
        }
    );

    if (response.status === 201 || response.status === 200) {
        closeReportModal();
        loadDashboardData(currentTab, currentPage);
    } else {
        alert('Gagal menyimpan draft.');
    }
}


async function submitReport() {
    if (editingReportId) {
        const saveResponse = await requestAPI(
            `/api/report/${editingReportId}/`,
            'PUT',
            {
                ...getReportFormData(),
                status: 'DRAFT'
            }
        );

        if (saveResponse.status !== 200) {
            alert('Gagal memperbarui draft sebelum diajukan.');
            return;
        }

        await submitDraft(editingReportId);
        closeReportModal();
        return;
    }

    const createResponse = await requestAPI(
        '/api/report/',
        'POST',
        getReportFormData()
    );

    if (createResponse.status === 201) {
        const id = createResponse.data.id;

        await submitDraft(id);
        closeReportModal();
    } else {
        alert('Gagal membuat laporan.');
    }
}


async function submitDraft(id) {
    const response = await requestAPI(
        `/api/report/${id}/submit/`,
        'POST'
    );

    if (response.status === 200) {
        loadDashboardData(currentTab, currentPage);
    } else {
        alert('Gagal mengajukan laporan.');
    }
}


function closeReportModal() {
    const modalElement = document.getElementById('reportModal');
    const modal = bootstrap.Modal.getInstance(modalElement);

    if (modal) {
        modal.hide();
    }

    document.getElementById('reportForm').reset();
    editingReportId = null;
}


function setupDashboardEvents() {
    document.getElementById('openCreateModalBtn').addEventListener(
        'click',
        openCreateModal
    );

    document.getElementById('myReportsTab').addEventListener(
        'click',
        function () {
            document.getElementById('myReportsTab').classList.add('active');
            document.getElementById('feedTab').classList.remove('active');
            loadDashboardData('my_reports', 1);
        }
    );

    document.getElementById('feedTab').addEventListener(
        'click',
        function () {
            document.getElementById('feedTab').classList.add('active');
            document.getElementById('myReportsTab').classList.remove('active');
            loadDashboardData('feed', 1);
        }
    );

    document.getElementById('saveDraftBtn').addEventListener(
        'click',
        saveDraft
    );

    document.getElementById('submitReportBtn').addEventListener(
        'click',
        submitReport
    );
}


function initDashboard() {
    setupDashboardEvents();
    loadDashboardData('my_reports', 1);
}


console.log('Smart City SPA Ready');