from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from main_app.models import Report

User = get_user_model()


class CRUDAndValidationTests(APITestCase):
    """
    MODUL 4
    Pengujian CRUD, Validasi Input, dan Pagination.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            username="warga",
            password="Password123!",
            is_admin=False
        )

        self.client.force_authenticate(user=self.user)

    # ======================================================
    # FT-01
    # Create report
    # ======================================================

    def test_FT_01_create_report(self):

        payload = {
            "title": "Lampu Jalan Mati",
            "category": "Infrastruktur",
            "description": "Lampu mati sejak kemarin",
            "location": "Bandar Lampung"
        }

        response = self.client.post(
            "/api/report/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        laporan = Report.objects.get(
            title="Lampu Jalan Mati"
        )

        self.assertEqual(
            laporan.reporter,
            self.user
        )

        self.assertEqual(
            laporan.status,
            "DRAFT"
        )

    # ======================================================
    # FT-02
    # title kosong
    # ======================================================

    def test_FT_02_title_kosong(self):

        payload = {
            "category": "Infrastruktur",
            "description": "Tes",
            "location": "Bandar Lampung"
        }

        response = self.client.post(
            "/api/report/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "title",
            response.data
        )

    # ======================================================
    # FT-03
    # description kosong
    # ======================================================

    def test_FT_03_description_kosong(self):

        payload = {
            "title": "Tes",
            "category": "Infrastruktur",
            "location": "Bandar Lampung"
        }

        response = self.client.post(
            "/api/report/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "description",
            response.data
        )

    # ======================================================
    # FT-04
    # XSS
    # ======================================================

    def test_FT_04_xss_disimpan(self):

        payload = {
            "title": "Tes XSS",
            "category": "Keamanan",
            "description": '<script>alert("xss")</script>',
            "location": "Lab"
        }

        response = self.client.post(
            "/api/report/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        laporan = Report.objects.get(
            title="Tes XSS"
        )

        self.assertIn(
            "script",
            laporan.description.lower()
        )

    # ======================================================
    # FT-05
    # pagination
    # ======================================================

    def test_FT_05_pagination(self):

        for i in range(15):
            Report.objects.create(
                title=f"Laporan {i}",
                category="A",
                description="B",
                location="C",
                reporter=self.user,
                status="REPORTED"
            )

        response = self.client.get(
            "/api/report/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            10
        )

    # ======================================================
    # FT-06
    # page_size
    # ======================================================

    def test_FT_06_page_size(self):

        for i in range(20):
            Report.objects.create(
                title=f"Data {i}",
                category="A",
                description="B",
                location="C",
                reporter=self.user,
                status="REPORTED"
            )

        response = self.client.get(
            "/api/report/?page_size=5"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(response.data["results"]),
            5
        )

    # ======================================================
    # FT-07
    # default queryset
    # ======================================================

    def test_FT_07_default_queryset(self):

        Report.objects.create(
            title="Draft",
            category="A",
            description="B",
            location="C",
            reporter=self.user,
            status="DRAFT"
        )

        Report.objects.create(
            title="Reported",
            category="A",
            description="B",
            location="C",
            reporter=self.user,
            status="REPORTED"
        )

        response = self.client.get(
            "/api/report/"
        )

        titles = [
            item["title"]
            for item in response.data["results"]
        ]

        self.assertIn(
            "Draft",
            titles
        )

        self.assertIn(
            "Reported",
            titles
        )

    # ======================================================
    # FT-08
    # delete draft sendiri
    # ======================================================

    def test_FT_08_delete_draft_sendiri(self):

        laporan = Report.objects.create(
            title="Draft Delete",
            category="A",
            description="B",
            location="C",
            reporter=self.user,
            status="DRAFT"
        )

        response = self.client.delete(
            f"/api/report/{laporan.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Report.objects.filter(pk=laporan.pk).exists()
        )

    # ======================================================
    # FT-09
    # delete reported ditolak
    # ======================================================

    def test_FT_09_delete_reported_ditolak(self):

        laporan = Report.objects.create(
            title="Reported Delete",
            category="A",
            description="B",
            location="C",
            reporter=self.user,
            status="REPORTED"
        )

        response = self.client.delete(
            f"/api/report/{laporan.pk}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # ======================================================
    # FT-10
    # user wajib login
    # ======================================================

    def test_FT_10_guest_tidak_bisa_create(self):

        self.client.logout()

        payload = {
            "title": "Tes",
            "category": "A",
            "description": "B",
            "location": "C"
        }

        response = self.client.post(
            "/api/report/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )