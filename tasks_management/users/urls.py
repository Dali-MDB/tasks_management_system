from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('refresh-token/', views.refresh_token, name='refresh_token'),
]   
