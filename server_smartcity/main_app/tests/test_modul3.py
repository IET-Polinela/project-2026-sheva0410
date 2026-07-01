from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from main_app.models import Report

User = get_user_model()


# ==========================================================
# MODUL 3A
# Workflow REST API
# ==========================================================

class WorkflowStateTests(APITestCase):

    def setUp(self):

        self.warga = User.objects.create_user(
            username="warga",
            password="Password123!",
            is_admin=False
        )

        self.admin = User.objects.create_user(
            username="admin",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.draft = Report.objects.create(
            title="Draft",
            category="Infrastruktur",
            description="Draft",
            location="Lampung",
            reporter=self.warga,
            status="DRAFT"
        )

        self.reported = Report.objects.create(
            title="Reported",
            category="Infrastruktur",
            description="Reported",
            location="Lampung",
            reporter=self.warga,
            status="REPORTED"
        )

        self.resolved = Report.objects.create(
            title="Resolved",
            category="Infrastruktur",
            description="Resolved",
            location="Lampung",
            reporter=self.warga,
            status="RESOLVED"
        )

    # ======================================================
    # WF-01
    # submit draft
    # ======================================================

    def test_WF_01_submit_draft(self):

        self.client.force_authenticate(user=self.warga)

        response = self.client.post(
            f"/api/report/{self.draft.pk}/submit/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.draft.refresh_from_db()

        self.assertEqual(
            self.draft.status,
            "REPORTED"
        )

    # ======================================================
    # WF-02
    # submit selain draft
    # ======================================================

    def test_WF_02_submit_reported_gagal(self):

        self.client.force_authenticate(user=self.warga)

        response = self.client.post(
            f"/api/report/{self.reported.pk}/submit/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    # ======================================================
    # WF-03
    # edit draft sendiri
    # ======================================================

    def test_WF_03_edit_draft_sendiri(self):

        self.client.force_authenticate(user=self.warga)

        payload = {
            "title": "Draft Baru",
            "category": self.draft.category,
            "description": self.draft.description,
            "location": self.draft.location,
            "status": "DRAFT"
        }

        response = self.client.put(
            f"/api/report/{self.draft.pk}/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.draft.refresh_from_db()

        self.assertEqual(
            self.draft.title,
            "Draft Baru"
        )

    # ======================================================
    # WF-04
    # edit reported ditolak
    # ======================================================

    def test_WF_04_edit_reported_ditolak(self):

        self.client.force_authenticate(user=self.warga)

        payload = {
            "title": "Baru",
            "category": self.reported.category,
            "description": self.reported.description,
            "location": self.reported.location,
            "status": "REPORTED"
        }

        response = self.client.put(
            f"/api/report/{self.reported.pk}/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # ======================================================
    # WF-05
    # edit resolved ditolak
    # ======================================================

    def test_WF_05_edit_resolved_ditolak(self):

        self.client.force_authenticate(user=self.warga)

        payload = {
            "title": "Resolved Baru",
            "category": self.resolved.category,
            "description": self.resolved.description,
            "location": self.resolved.location,
            "status": "RESOLVED"
        }

        response = self.client.put(
            f"/api/report/{self.resolved.pk}/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    # ======================================================
    # WF-06
    # submit milik orang lain
    # ======================================================

    def test_WF_06_submit_milik_orang_lain(self):

        user2 = User.objects.create_user(
            username="user2",
            password="Password123!"
        )

        draft = Report.objects.create(
            title="Draft2",
            category="A",
            description="B",
            location="C",
            reporter=user2,
            status="DRAFT"
        )

        self.client.force_authenticate(user=self.warga)

        response = self.client.post(
            f"/api/report/{draft.pk}/submit/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


# ==========================================================
# MODUL 3B
# Workflow Admin
# ==========================================================

class AdminWorkflowTests(APITestCase):

    def setUp(self):

        self.admin = User.objects.create_user(
            username="admin",
            password="Admin123!",
            is_admin=True,
            is_staff=True
        )

        self.report = Report.objects.create(
            title="Laporan",
            category="Infrastruktur",
            description="Test",
            location="Bandar Lampung",
            reporter=self.admin,
            status="REPORTED"
        )

    # ======================================================
    # WF-07
    # Reported -> Verified
    # ======================================================

    def test_WF_07_admin_valid_transition(self):

        self.client.force_authenticate(user=self.admin)

        payload = {
            "status": "VERIFIED"
        }

        response = self.client.put(
            f"/api/report/{self.report.pk}/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.report.refresh_from_db()

        self.assertEqual(
            self.report.status,
            "VERIFIED"
        )

    # ======================================================
    # WF-08
    # lompat status
    # ======================================================

    def test_WF_08_admin_invalid_transition(self):

        self.client.force_authenticate(user=self.admin)

        payload = {
            "status": "RESOLVED"
        }

        response = self.client.put(
            f"/api/report/{self.report.pk}/",
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    # ======================================================
    # WF-09
    # VERIFIED -> IN_PROGRESS
    # ======================================================

    def test_WF_09_verified_ke_in_progress(self):

        self.report.status = "VERIFIED"
        self.report.save()

        self.client.force_authenticate(user=self.admin)

        response = self.client.put(
            f"/api/report/{self.report.pk}/",
            {
                "status": "IN_PROGRESS"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # ======================================================
    # WF-10
    # IN_PROGRESS -> RESOLVED
    # ======================================================

    def test_WF_10_in_progress_ke_resolved(self):

        self.report.status = "IN_PROGRESS"
        self.report.save()

        self.client.force_authenticate(user=self.admin)

        response = self.client.put(
            f"/api/report/{self.report.pk}/",
            {
                "status": "RESOLVED"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )