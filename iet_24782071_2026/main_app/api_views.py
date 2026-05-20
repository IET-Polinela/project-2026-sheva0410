from rest_framework import viewsets
from rest_framework import permissions

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOnly


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraftOnly
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)