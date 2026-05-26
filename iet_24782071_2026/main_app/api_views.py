from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerDraftOrAdminStatusOnly


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_admin:
            return Report.objects.exclude(status='DRAFT').order_by('-created_at')

        return Report.objects.filter(
            Q(status__in=['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']) |
            Q(reporter=user)
        ).order_by('-created_at')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'submit']:
            return [
                permissions.IsAuthenticated(),
                IsOwnerDraftOrAdminStatusOnly()
            ]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(
            reporter=self.request.user,
            status='DRAFT'
        )

    def update(self, request, *args, **kwargs):
        report = self.get_object()

        if request.user.is_admin:
            old_status = report.status
            new_status = request.data.get('status')

            valid_transitions = {
                'REPORTED': 'VERIFIED',
                'VERIFIED': 'IN_PROGRESS',
                'IN_PROGRESS': 'RESOLVED',
            }

            if valid_transitions.get(old_status) != new_status:
                return Response(
                    {'detail': 'Transisi status tidak valid untuk admin.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            report.status = new_status
            report.save()

            serializer = self.get_serializer(report)
            return Response(serializer.data)

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        report = self.get_object()

        if report.reporter != request.user:
            return Response(
                {'detail': 'Anda bukan pemilik laporan ini.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if report.status != 'DRAFT':
            return Response(
                {'detail': 'Hanya laporan DRAFT yang dapat disubmit.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        report.status = 'REPORTED'
        report.save()

        serializer = self.get_serializer(report)
        return Response(serializer.data)