from django.core.validators import FileExtensionValidator
from django.db import models


class Sight(models.Model):
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    title_kg = models.CharField(max_length=255)

    short_description_ru = models.TextField(blank=True)
    short_description_en = models.TextField(blank=True)
    short_description_kg = models.TextField(blank=True)

    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_kg = models.TextField(blank=True)

    main_image = models.ImageField(
        upload_to='sights/main/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', '-id')

    def __str__(self):
        return self.title_ru


class SightImage(models.Model):
    sight = models.ForeignKey(Sight, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='sights/gallery/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
    )
    title_ru = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)
    title_kg = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order', 'id')

    def __str__(self):
        return f'{self.sight_id}#{self.id}'
