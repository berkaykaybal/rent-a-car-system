from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('verify/', views.verify_profile_view, name='verify_profile'),
    path('login/', views.user_login, name='user_login'),
    
    path('logout/', views.user_logout, name='user_logout'),
]