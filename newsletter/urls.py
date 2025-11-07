from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe_view, name='newsletter_subscribe'),
    path('unsubscribe/<str:email>/', views.newsletter_unsubscribe_view, name='newsletter_unsubscribe'),
]
