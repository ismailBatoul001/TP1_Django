from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('profile/<int:id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('activity/new/', views.create_activity, name='create_activity'),
    path('activity/<int:pk>/subscribe/', views.subscribe_activity, name='subscribe_activity'),
    path('activity/<int:pk>/unsubscribe/', views.unsubscribe_activity, name='unsubscribe_activity'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path("logout/", views.custom_logout, name="logout"),
    path("signup/", views.register, name="signup"),
    path("", views.base, name="home"),
]