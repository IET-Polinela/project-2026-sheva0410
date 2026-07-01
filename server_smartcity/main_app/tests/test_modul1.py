from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(APITestCase):
    """
    MODUL 1
    Pengujian Otorisasi dan Manajemen Sesi

    Fokus:
    - Login JWT
    - Login gagal
    - Pembatasan akses halaman admin
    """

    def setUp(self):
        self.warga = User.objects.create_user(
            username="warga_test",
            password="Password123!",
            is_admin=False
        )

        self.admin = User.objects.create_user(
            username="admin_test",
            password="AdminPass123!",
            is_admin=True,
            is_staff=True
        )

    # ==========================================================
    # AUTH-01
    # Login berhasil memperoleh JWT
    # ==========================================================

    def test_AUTH_01_login_valid(self):

        url = reverse("token_obtain_pair")

        response = self.client.post(
            url,
            {
                "username": "warga_test",
                "password": "Password123!"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # ==========================================================
    # AUTH-02
    # Password salah
    # ==========================================================

    def test_AUTH_02_login_invalid_password(self):

        url = reverse("token_obtain_pair")

        response = self.client.post(
            url,
            {
                "username": "warga_test",
                "password": "SALAHPASSWORD"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertNotIn("access", response.data)

    # ==========================================================
    # AUTH-03
    # Warga tidak boleh membuka halaman Create Report
    # ==========================================================

    def test_AUTH_03_warga_tidak_bisa_create_report(self):

        self.client.login(
            username="warga_test",
            password="Password123!"
        )

        response = self.client.get(
            reverse("create_report")
        )

        self.assertEqual(response.status_code, 302)

    # ==========================================================
    # AUTH-04
    # Admin boleh membuka halaman Create
    # ==========================================================

    def test_AUTH_04_admin_boleh_create_report(self):

        self.client.login(
            username="admin_test",
            password="AdminPass123!"
        )

        response = self.client.get(
            reverse("create_report")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ==========================================================
    # AUTH-05
    # Anonymous diarahkan ke login
    # ==========================================================

    def test_AUTH_05_guest_redirect_login(self):

        response = self.client.get(
            reverse("report_list")
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertIn("/login/", response.url)

    # ==========================================================
    # AUTH-06
    # Admin dapat mengakses daftar laporan
    # ==========================================================

    def test_AUTH_06_admin_dapat_report_list(self):

        self.client.login(
            username="admin_test",
            password="AdminPass123!"
        )

        response = self.client.get(
            reverse("report_list")
        )

        self.assertEqual(
            response.status_code,
            200
        )