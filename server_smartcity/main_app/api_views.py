from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerDraftOrAdminStatusOnly


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user
        tab = self.request.query_params.get('tab', None)

        queryset = Report.objects.all().order_by('-updated_at')

        if user.is_admin:
            return queryset.exclude(status='DRAFT')

        if tab == 'my_reports':
            return queryset.filter(reporter=user)

        if tab == 'feed':
            return queryset.filter(
                ~Q(reporter=user) &
                ~Q(status='DRAFT')
            )

        return queryset.filter(
            ~Q(status='DRAFT') |
            Q(status='DRAFT', reporter=user)
        )

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