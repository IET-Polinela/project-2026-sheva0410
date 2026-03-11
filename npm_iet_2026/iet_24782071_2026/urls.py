from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Halaman Utama")

def welcome(request):
    return HttpResponse("Selamat Datang")

urlpatterns = [
    path('', home),
    path('welcome/', welcome),
    path('admin/', admin.site.urls),
]