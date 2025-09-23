from django.contrib import admin
from .models import Category, Activity
from django.contrib.auth import get_user_model


# Register your models here.
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'avatar', 'bio', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_city', 'start_time', 'end_time', 'proposer', 'category')
    search_fields = ('title', 'location_city', 'description')
    list_filter = ('location_city', 'start_time', 'end_time', 'category')
