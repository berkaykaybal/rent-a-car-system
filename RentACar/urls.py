from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vehicles.urls')),
    path('register/', account_views.register_view, name='register'),
    path('verify/', account_views.verify_profile_view, name='verify_profile'),
    path('login/', account_views.user_login, name='user_login'),
    path('logout/', account_views.user_logout, name='user_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)