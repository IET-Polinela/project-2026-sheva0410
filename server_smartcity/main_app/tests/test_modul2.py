from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from main_app.models import Report

User = get_user_model()


class PrivacyAndDataHidingTests(APITestCase):
    """
    MODUL 2
    Pengujian Privasi Data dan Visibilitas Laporan.
    """

    def setUp(self):
        self.warga_a = User.objects.create_user(
            username="warga_a",
            password="Password123!",
            is_admin=False
        )

        self.warga_b = User.objects.create_user(
            username="warga_b",
            password="Password123!",
            is_admin=False
        )

        self.admin = User.objects.create_user(
            username="admin",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.draft_b = Report.objects.create(
            title="Draft B",
            category="Infrastruktur",
            description="Draft milik B",
            location="Bandar Lampung",
            reporter=self.warga_b,
            status="DRAFT"
        )

        self.report_a = Report.objects.create(
            title="Report A",
            category="Infrastruktur",
            description="Report milik A",
            location="Bandar Lampung",
            reporter=self.warga_a,
            status="REPORTED"
        )

        self.report_b = Report.objects.create(
            title="Report B",
            category="Kebersihan",
            description="Report milik B",
            location="Metro",
            reporter=self.warga_b,
            status="REPORTED"
        )

    # ==========================================================
    # PRIV-01
    # Feed hanya menampilkan laporan publik orang lain
    # ==========================================================

    def test_PRIV_01_feed_hanya_menampilkan_laporan_publik(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=feed")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        titles = [r["title"] for r in results]

        self.assertIn("Report B", titles)

        self.assertNotIn("Draft B", titles)

        self.assertNotIn("Report A", titles)

    # ==========================================================
    # PRIV-02
    # Tab my_reports hanya menampilkan laporan sendiri
    # ==========================================================

    def test_PRIV_02_my_reports_hanya_milik_sendiri(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=my_reports")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]

        self.assertEqual(len(results), 1)

        self.assertEqual(results[0]["title"], "Report A")

    # ==========================================================
    # PRIV-03
    # Reporter selalu anonim
    # ==========================================================

    def test_PRIV_03_reporter_selalu_anonim(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=feed")

        laporan = response.data["results"][0]

        self.assertEqual(
            laporan["reporter"],
            "Warga Anonim"
        )

    # ==========================================================
    # PRIV-04
    # is_owner False pada feed
    # ==========================================================

    def test_PRIV_04_is_owner_false_pada_feed(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=feed")

        laporan = response.data["results"][0]

        self.assertFalse(
            laporan["is_owner"]
        )

    # ==========================================================
    # PRIV-05
    # is_owner True pada my_reports
    # ==========================================================

    def test_PRIV_05_is_owner_true_pada_my_reports(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/?tab=my_reports")

        laporan = response.data["results"][0]

        self.assertTrue(
            laporan["is_owner"]
        )

    # ==========================================================
    # PRIV-06
    # Draft orang lain tidak muncul pada endpoint default
    # ==========================================================

    def test_PRIV_06_draft_orang_lain_tidak_terlihat(self):

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [
            item["title"]
            for item in response.data["results"]
        ]

        self.assertNotIn(
            "Draft B",
            titles
        )

    # ==========================================================
    # PRIV-07
    # Draft sendiri tetap muncul
    # ==========================================================

    def test_PRIV_07_draft_sendiri_muncul(self):

        Report.objects.create(
            title="Draft Saya",
            category="Infrastruktur",
            description="draft",
            location="Bandung",
            reporter=self.warga_a,
            status="DRAFT"
        )

        self.client.force_authenticate(user=self.warga_a)

        response = self.client.get("/api/report/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [
            item["title"]
            for item in response.data["results"]
        ]

        self.assertIn(
            "Draft Saya",
            titles
        )

    # ==========================================================
    # PRIV-08
    # Admin melihat semua kecuali draft
    # ==========================================================

    def test_PRIV_08_admin_melihat_semua_non_draft(self):

        self.client.force_authenticate(user=self.admin)

        response = self.client.get("/api/report/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        titles = [
            item["title"]
            for item in response.data["results"]
        ]

        self.assertIn("Report A", titles)

        self.assertIn("Report B", titles)

        self.assertNotIn("Draft B", titles)