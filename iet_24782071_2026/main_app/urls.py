from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_report, name='create_report'),
    path('update/<int:id>/', views.update_report, name='update_report'),
    path('delete/<int:id>/', views.delete_report, name='delete_report'),
]