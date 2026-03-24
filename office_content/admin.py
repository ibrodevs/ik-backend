from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from ckeditor.widgets import CKEditorWidget

from .models import LeadershipMember, OfficialDocument, ProcurementItem, Project


@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name_ru', 'position_ru', 'order', 'is_active', 'photo_preview')
    list_filter = ('is_active',)
    search_fields = (
        'full_name_ru',
        'full_name_en',
        'full_name_kg',
        'position_ru',
        'position_en',
        'position_kg',
    )
    ordering = ('order', 'id')

    @admin.display(description='Фото')
    def photo_preview(self, obj):
        if not obj.photo:
            return '-'
        return format_html(
            '<img src="{}" width="40" height="40" style="object-fit:cover;border-radius:4px;"/>',
            obj.photo.url,
        )


@admin.register(OfficialDocument)
class OfficialDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'category', 'order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('order', 'id')


@admin.register(ProcurementItem)
class ProcurementItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'type', 'amount_som', 'deadline', 'order', 'is_active')
    list_filter = ('is_active', 'type')
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('order', 'deadline', 'id')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_ru', 'type', 'order', 'is_active', 'image_preview')
    list_filter = ('is_active', 'type')
    search_fields = ('title_ru', 'title_en', 'title_kg')
    ordering = ('order', 'id')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget},
    }

    @admin.display(description='Превью')
    def image_preview(self, obj):
        if not obj.image:
            return '-'
        return format_html(
            '<img src="{}" width="60" height="40" style="object-fit:cover;border-radius:4px;"/>',
            obj.image.url,
        )
