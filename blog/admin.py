from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Like


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    summernote_fields = ('content',)
    list_editable = ['status']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'post')
