from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_approved', 'created_at', 'approved_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at', 'approved_at']
    list_editable = ['is_approved']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
