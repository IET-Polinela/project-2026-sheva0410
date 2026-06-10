from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportUpdateStatusView,
    ReportSearchView,        
    ReportDetailAPIView      
)

urlpatterns = [
    #  HOME 
    path('', TemplateView.as_view(template_name='main_app/home.html'), name='home'),

    # REPORTS
    path('reports/', ReportListView.as_view(), name='report_list'),

    path('detail/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
    path('create/', ReportCreateView.as_view(), name='create_report'),
    path('update/<int:pk>/', ReportUpdateView.as_view(), name='update_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),
    path('update-status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),

    path('search/', ReportSearchView.as_view(), name='search'),
    path('api/detail/<int:pk>/', ReportDetailAPIView.as_view(), name='api_detail'),
]