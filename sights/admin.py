from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget

from .models import Sight, SightImage


class SightImageInline(admin.TabularInline):
    model = SightImage
    extra = 0
    fields = ('image', 'order', 'title_ru', 'title_en', 'title_kg')
    ordering = ('order', 'id')


@admin.register(Sight)
class SightAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'is_active', 'thumb')
    list_filter = ('is_active',)
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('-created_at', '-id')
    inlines = (SightImageInline,)
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    @admin.display(description='Preview')
    def thumb(self, obj):
        if not obj.main_image:
            return '-'
        return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.main_image.url)


@admin.register(SightImage)
class SightImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sight', 'order', 'thumb')
    list_filter = ('sight',)
    ordering = ('order', 'id')

    @admin.display(description='Preview')
    def thumb(self, obj):
        if not obj.image:
            return '-'
        return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
