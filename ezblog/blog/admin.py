from django.contrib import admin

from .models import Category, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', ]
    list_display_links = ['id', 'title', ]
    ordering = ['-created_at', 'id', ]
    search_fields = ['title', 'content', ]
    date_hierarchy = 'created_at'
    list_filter = ['tags', ]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

