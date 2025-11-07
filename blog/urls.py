from django.urls import path
from . import views

urlpatterns = [
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    path('post/<slug:slug>/like/', views.post_like_view, name='post_like'),
    path('search/', views.search_view, name='search'),
]
