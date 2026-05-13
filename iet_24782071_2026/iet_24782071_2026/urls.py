from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [

    # ADMIN
    path('admin/', admin.site.urls),

    
    # API DRF
    path('api/', include('main_app.api_urls')),


    # DASHBOARD
    path('', include('dashboard_24782071.urls')),


    # MAIN APP
    path('', include('main_app.urls')),

    
    # ABOUT
    path('about/', include('about.urls')),


    # CONTACTS
    path('contacts/', include('contacts.urls')),


    # USER MANAGEMENT
    path('', include('usermanagement_24782071.urls')),


    # LOGIN
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),


    # LOGOUT
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/',
            http_method_names=['get', 'post']
        ),
        name='logout'
    ),

]