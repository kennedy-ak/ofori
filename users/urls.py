from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/approve-user/<int:user_id>/', views.approve_user_view, name='approve_user'),
    path('user/<str:username>/', views.user_profile_view, name='user_profile'),
]
