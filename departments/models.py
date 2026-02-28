from django.core.validators import FileExtensionValidator
from django.db import models


class DepartmentCategory(models.Model):
    name_ru = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    name_kg = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return self.name_ru


class Department(models.Model):
    icon = models.FileField(
        upload_to='departments/icons/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'svg'])],
    )
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    short_description_ru = models.TextField(blank=True)
    short_description_en = models.TextField(blank=True)
    short_description_kg = models.TextField(blank=True)

    category = models.ForeignKey(DepartmentCategory, related_name='departments', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return self.title_ru


class DepartmentLeader(models.Model):
    department = models.OneToOneField(Department, related_name='leader', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to='departments/leaders/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )

    position_ru = models.CharField(max_length=255)
    position_en = models.CharField(max_length=255)
    position_kg = models.CharField(max_length=255)

    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    address_ru = models.CharField(max_length=255, blank=True)
    address_en = models.CharField(max_length=255, blank=True)
    address_kg = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name
