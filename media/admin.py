from django.contrib import admin
from django.utils.html import format_html

from .models import MediaCategory, MediaItem


@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order', 'id')
    search_fields = ('name_ru', 'name_en', 'name_kg', 'slug')


@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'category', 'type', 'order', 'is_active', 'preview')
    list_filter = ('is_active', 'category', 'type')
    ordering = ('order', '-created_at', '-id')
    search_fields = ('title_ru', 'title_en', 'title_kg')

    @admin.display(description='Preview')
    def preview(self, obj):
        file_name = str(obj.file.name).lower() if obj.file else ''
        if obj.type == MediaItem.TYPE_VIDEO:
            if obj.preview_image:
                return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.preview_image.url)
            return 'VIDEO'
        if any(file_name.endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.webp')):
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.file.url)
        return '-'
