from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget

from .models import Department, DepartmentCategory, DepartmentLeader


@admin.register(DepartmentCategory)
class DepartmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_ru', 'name_en', 'name_kg', 'slug')
    ordering = ('order', 'id')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'category', 'order', 'is_active', 'icon_preview')
    list_filter = ('is_active', 'category')
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('order', 'id')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    @admin.display(description='Icon')
    def icon_preview(self, obj):
        if not obj.icon:
            return '-'
        if str(obj.icon.name).lower().endswith('.svg'):
            return 'SVG'
        return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.icon.url)


@admin.register(DepartmentLeader)
class DepartmentLeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'department', 'email', 'phone', 'photo_preview')
    list_filter = ('department',)
    search_fields = ('full_name', 'position_ru', 'position_en', 'position_kg')

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        if not obj.photo:
            return '-'
        return format_html('<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.photo.url)
