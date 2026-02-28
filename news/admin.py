from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget

from .models import News, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_ru', 'slug', 'order', 'is_active')
    list_filter = ('is_active',)
    ordering = ('order', 'id')
    search_fields = ('name_ru', 'name_en', 'name_kg', 'slug')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'category', 'date', 'is_hot', 'is_main', 'is_active', 'thumb')
    list_filter = ('is_active', 'category', 'is_hot', 'is_main')
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('-date', '-id')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    @admin.display(description='Preview')
    def thumb(self, obj):
        if not obj.image:
            return '-'
        return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
