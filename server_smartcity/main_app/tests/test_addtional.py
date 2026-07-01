from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase, APIRequestFactory

from main_app.models import Report
from main_app.serializers import ReportSerializer

User = get_user_model()


# ==========================================================
# ADDITIONAL 1
# MODEL & SERIALIZER COVERAGE
# ==========================================================

class SerializerAndModelCoverageTests(APITestCase):
    """
    Coverage tambahan untuk models.py dan serializers.py
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="coverage_user",
            password="Password123!",
            is_admin=False
        )

        self.report = Report.objects.create(
            title="Laporan Coverage",
            category="Infrastruktur",
            description="Deskripsi coverage",
            location="Bandar Lampung",
            reporter=self.user,
            status="REPORTED"
        )

    # ======================================================
    # ADD-01
    # __str__()
    # ======================================================

    def test_ADD_01_report_str(self):

        self.assertEqual(
            str(self.report),
            "Laporan Coverage"
        )

    # ======================================================
    # ADD-02
    # serializer tanpa request
    # ======================================================

    def test_ADD_02_serializer_no_request(self):

        serializer = ReportSerializer(
            self.report,
            context={}
        )

        self.assertEqual(
            serializer.data["reporter"],
            "Warga Anonim"
        )

        self.assertFalse(
            serializer.data["is_owner"]
        )

    # ======================================================
    # ADD-03
    # serializer owner
    # ======================================================

    def test_ADD_03_serializer_owner(self):

        factory = APIRequestFactory()

        request = factory.get("/")

        request.user = self.user

        serializer = ReportSerializer(
            self.report,
            context={
                "request": request
            }
        )

        self.assertTrue(
            serializer.data["is_owner"]
        )

    # ======================================================
    # ADD-04
    # serializer bukan owner
    # ======================================================

    def test_ADD_04_serializer_not_owner(self):

        other = User.objects.create_user(
            username="other_user",
            password="Password123!"
        )

        factory = APIRequestFactory()

        request = factory.get("/")

        request.user = other

        serializer = ReportSerializer(
            self.report,
            context={
                "request": request
            }
        )

        self.assertFalse(
            serializer.data["is_owner"]
        )

        self.assertEqual(
            serializer.data["reporter"],
            "Warga Anonim"
        )
# ==========================================================
# ADDITIONAL 2
# LIST VIEW, SEARCH, DETAIL VIEW & API
# ==========================================================

class ViewCoverageTests(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username="admin_view",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="user_view",
            password="Password123!",
            is_admin=False
        )

        self.report = Report.objects.create(
            title="Lampu Jalan Mati",
            category="Infrastruktur",
            description="Lampu mati sejak kemarin",
            location="Bandar Lampung",
            reporter=self.user,
            status="REPORTED"
        )

    # ======================================================
    # ADD-05
    # Home View
    # ======================================================

    def test_ADD_05_home_view(self):

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/home.html"
        )

    # ======================================================
    # ADD-06
    # Report List (Admin)
    # ======================================================

    def test_ADD_06_report_list_admin(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse("report_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/reports.html"
        )

    # ======================================================
    # ADD-07
    # Report List (Citizen)
    # ======================================================

    def test_ADD_07_report_list_citizen(self):

        self.client.login(
            username="user_view",
            password="Password123!"
        )

        response = self.client.get(
            reverse("report_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/reports.html"
        )

    # ======================================================
    # ADD-08
    # Search berdasarkan title
    # ======================================================

    def test_ADD_08_search_title(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse("search"),
            {
                "q": "Lampu"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.json()

        self.assertEqual(
            len(data),
            1
        )

        self.assertEqual(
            data[0]["title"],
            "Lampu Jalan Mati"
        )

    # ======================================================
    # ADD-09
    # Search berdasarkan status
    # ======================================================

    def test_ADD_09_search_status(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse("search"),
            {
                "status": "REPORTED"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.json()),
            1
        )

    # ======================================================
    # ADD-10
    # Search berdasarkan kategori
    # ======================================================

    def test_ADD_10_search_category(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse("search"),
            {
                "category": "Infrastruktur"
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.json()),
            1
        )

    # ======================================================
    # ADD-11
    # Detail API
    # ======================================================

    def test_ADD_11_detail_api(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse(
                "api_detail",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        data = response.json()

        self.assertEqual(
            data["title"],
            "Lampu Jalan Mati"
        )

        self.assertEqual(
            data["category"],
            "Infrastruktur"
        )

        self.assertEqual(
            data["location"],
            "Bandar Lampung"
        )

        self.assertEqual(
            data["status"],
            "REPORTED"
        )

    # ======================================================
    # ADD-12
    # Detail View
    # ======================================================

    def test_ADD_12_detail_view(self):

        self.client.login(
            username="admin_view",
            password="Admin123!"
        )

        response = self.client.get(
            reverse(
                "report_detail",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/detail.html"
        )   

# ==========================================================
# ADDITIONAL 3
# UPDATE STATUS VIEW COVERAGE
# ==========================================================

class UpdateStatusViewCoverageTests(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username="admin_status",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="user_status",
            password="Password123!",
            is_admin=False
        )

        self.report = Report.objects.create(
            title="Lampu Rusak",
            category="Infrastruktur",
            description="Lampu mati",
            location="Bandar Lampung",
            reporter=self.user,
            status="REPORTED"
        )

    # ======================================================
    # ADD-13
    # Guest diarahkan ke login
    # ======================================================

    def test_ADD_13_guest_redirect(self):

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "VERIFIED"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # ======================================================
    # ADD-14
    # Citizen ditolak mengubah status
    # ======================================================

    def test_ADD_14_citizen_rejected(self):

        self.client.login(
            username="user_status",
            password="Password123!"
        )

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "VERIFIED"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "REPORTED"
        )

    # ======================================================
    # ADD-15
    # Admin REPORTED -> VERIFIED
    # ======================================================

    def test_ADD_15_admin_reported_to_verified(self):

        self.client.login(
            username="admin_status",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "VERIFIED"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "VERIFIED"
        )

    # ======================================================
    # ADD-16
    # Admin tidak boleh lompat status
    # ======================================================

    def test_ADD_16_invalid_transition(self):

        self.client.login(
            username="admin_status",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "RESOLVED"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "REPORTED"
        )

    # ======================================================
    # ADD-17
    # VERIFIED -> IN_PROGRESS
    # ======================================================

    def test_ADD_17_verified_to_in_progress(self):

        self.report.status = "VERIFIED"
        self.report.save()

        self.client.login(
            username="admin_status",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "IN_PROGRESS"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "IN_PROGRESS"
        )

    # ======================================================
    # ADD-18
    # IN_PROGRESS -> RESOLVED
    # ======================================================

    def test_ADD_18_in_progress_to_resolved(self):

        self.report.status = "IN_PROGRESS"
        self.report.save()

        self.client.login(
            username="admin_status",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "update_status",
                kwargs={"pk": self.report.pk}
            ),
            {
                "status": "RESOLVED"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "RESOLVED"
        )

# ==========================================================
# ADDITIONAL 4
# CREATE, UPDATE, DELETE VIEW COVERAGE
# ==========================================================

class CRUDViewCoverageTests(TestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username="admin_crud",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="user_crud",
            password="Password123!",
            is_admin=False
        )

        self.report = Report.objects.create(
            title="Laporan Awal",
            category="Infrastruktur",
            description="Deskripsi awal",
            location="Bandar Lampung",
            reporter=self.user,
            status="REPORTED"
        )

    # ======================================================
    # ADD-19
    # Admin membuka halaman create
    # ======================================================

    def test_ADD_19_create_get_admin(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.get(
            reverse("create_report")
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "main_app/create_report.html"
        )

    # ======================================================
    # ADD-20
    # Citizen tidak boleh create
    # ======================================================

    def test_ADD_20_create_citizen_rejected(self):

        self.client.login(
            username="user_crud",
            password="Password123!"
        )

        response = self.client.get(
            reverse("create_report")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # ======================================================
    # ADD-21
    # Admin create berhasil
    # ======================================================

    def test_ADD_21_create_post(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.post(
            reverse("create_report"),
            {
                "title": "Laporan Baru",
                "category": "Infrastruktur",
                "description": "Deskripsi baru",
                "location": "Metro"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertTrue(
            Report.objects.filter(
                title="Laporan Baru"
            ).exists()
        )

    # ======================================================
    # ADD-22
    # Admin membuka update
    # ======================================================

    def test_ADD_22_update_get(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.get(
            reverse(
                "update_report",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/update_report.html"
        )

    # ======================================================
    # ADD-23
    # Admin update berhasil
    # ======================================================

    def test_ADD_23_update_post(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "update_report",
                kwargs={
                    "pk": self.report.pk
                }
            ),
            {
                "title": "Judul Baru",
                "category": "Infrastruktur",
                "description": "Update",
                "location": "Jakarta"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.title,
            "Judul Baru"
        )

    # ======================================================
    # ADD-24
    # Citizen tidak boleh update
    # ======================================================

    def test_ADD_24_update_citizen_rejected(self):

        self.client.login(
            username="user_crud",
            password="Password123!"
        )

        response = self.client.get(
            reverse(
                "update_report",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # ======================================================
    # ADD-25
    # Admin membuka delete
    # ======================================================

    def test_ADD_25_delete_get(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.get(
            reverse(
                "delete_report",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            "main_app/delete_report.html"
        )

    # ======================================================
    # ADD-26
    # Citizen tidak boleh delete
    # ======================================================

    def test_ADD_26_delete_citizen_rejected(self):

        self.client.login(
            username="user_crud",
            password="Password123!"
        )

        response = self.client.get(
            reverse(
                "delete_report",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

    # ======================================================
    # ADD-27
    # Admin delete berhasil
    # ======================================================

    def test_ADD_27_delete_post(self):

        self.client.login(
            username="admin_crud",
            password="Admin123!"
        )

        response = self.client.post(
            reverse(
                "delete_report",
                kwargs={
                    "pk": self.report.pk
                }
            )
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertFalse(
            Report.objects.filter(
                pk=self.report.pk
            ).exists()
        )