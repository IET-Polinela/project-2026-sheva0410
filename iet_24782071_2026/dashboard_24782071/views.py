from django.views.generic import TemplateView
from django.http import JsonResponse
from main_app.models import Report
from django.db.models import Count


# HALAMAN DASHBOARD
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'


# API DATA DASHBOARD (JSON)
class DashboardDataView(TemplateView):
    def get(self, request, *args, **kwargs):

        
        #  STATUS DISTRIBUTION
      
        status_data = (
            Report.objects
            .values('status')
            .annotate(total=Count('status'))
        )

       
        #  CATEGORY DISTRIBUTION
        
        category_data = (
            Report.objects
            .values('category')
            .annotate(total=Count('category'))
        )

        
        # 5 TERBARU REPORTED
        
        latest_reported = list(
            Report.objects
            .filter(status='REPORTED')
            .order_by('-id')[:5]
            .values('title', 'location', 'status')
        )

       
        # 5 TERBARU RESOLVED
        
        latest_resolved = list(
            Report.objects
            .filter(status='RESOLVED')
            .order_by('-id')[:5]
            .values('title', 'location', 'status')
        )

        # RETURN JSON
        return JsonResponse({
            'status': list(status_data),
            'category': list(category_data),
            'latest_reported': latest_reported,
            'latest_resolved': latest_resolved,
        })