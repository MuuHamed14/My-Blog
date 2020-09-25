from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_filter = ['active', 'created_at','created_by']
    list_display = ['title', 'created_at', 'active','created_by']
    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
