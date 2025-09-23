from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('activity/new/', views.create_activity, name='create_activity'),
    path('activity/<int:pk>/subscribe/', views.subscribe_activity, name='subscribe_activity'),
    path('activity/<int:pk>/unsubscribe/', views.unsubscribe_activity, name='unsubscribe_activity'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path("logout/", views.custom_logout, name="logout"),
    path("signup/", views.register, name="signup"),
    path("", views.base, name="home"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)